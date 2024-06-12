from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import random
import json


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['gameID']
        self.game = get_object_or_404(Game, id=self.game_id)
        self.game_name = f'game_{self.game_id}'
        

        print(f"{self.user.username} connected to game {self.game_id}")

        async_to_sync(self.channel_layer.group_add)(
            self.game_name, self.channel_name
        )

        self.accept()

        context = {
            'game': self.game,
            'user': self.user,
        }

        if self.game.game_state == 0:
            html = render_to_string('partials/game_select_slot.html', context)
            self.send(text_data=html)
        elif self.game.game_state == 1:
            html = render_to_string('partials/game_in.html', context)
            self.send(text_data=html)
        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)


        if self.user != self.game.player1 and self.user != self.game.player2:
            return

        # update game object
        self.game = Game.objects.get(id=self.game_id)

        action = data['action']
        if action == 'select-slot':
            self.handleSelectSlot(data)
            
        elif action == 'shoot':
            self.handleShoot(data)

        elif action == 'pass':
            print("DEBUG: pass")
            self.handlePass(data)
    

    def update_notification_handler(self, event):
        self.game = Game.objects.get(id=self.game_id)
        context = {
            'game': self.game,
            'user': self.user,
            'response': event['response'],
            'message': event['message'],
        }
        print(f"DEBUG: message: {event['message']}, response: { event['response']}")
        html = render_to_string('partials/game_notification.html', context)
        self.send(text_data=html)


    def update_gamePage_handler(self, event):
        self.game = Game.objects.get(id=self.game_id)

        context = {
            'game': self.game,
            'user': self.user,
            'response': event['response'],
            'message': event['message'],
        }
        html = render_to_string('partials/game_in.html', context)
        self.send(text_data=html)



    def handleSelectSlot(self, data):
        if self.game.game_state != 0:
            return
        
        slot1 = int(data['slot1'])
        slot2 = int(data['slot2'])
        slot3 = int(data['slot3'])
        
        # validate the data
        if not validateSlots(slot1, slot2, slot3):
            context = {
                'game': self.game,
                'user': self.user,
                'response': 'failed',
                'message': 'Invalid slots! Please select diffent numbers from 1 to 24.'
            }
            html = render_to_string('partials/game_notification.html', context)
            self.send(text_data=html)
            return
        
        

        print(f"current game.player1_slots: {self.game.player1_slots}")
        print(f"current game.player2_slots: {self.game.player2_slots}")
        # if player has selected the slots
        if (self.user == self.game.player1 and self.game.player1_slots != '0,0,0') \
        or (self.user == self.game.player2 and self.game.player2_slots != '0,0,0'):
            print(f"DEBUG: {self.user.username} has already selected the slots!")
            context = {
                'game': self.game,
                'user': self.user,
                'response': 'failed',
                'message': 'You have already selected the slots!'
            }
            html = render_to_string('partials/game_notification.html', context)
            self.send(text_data=html)
            return 
        
        # put these slots into the database and update
        if self.user == self.game.player1:
            self.game.player1_slots = f'{slot1},{slot2},{slot3}'
        else:
            self.game.player2_slots = f'{slot1},{slot2},{slot3}'
        
        
        print(f"player1_slots: {self.game.player1_slots}")
        print(f"player2_slots: {self.game.player2_slots}")

        # check if both players have selected their slots and not repetative
        if self.game.player1_slots != '0,0,0' and self.game.player2_slots != '0,0,0':
            # if overlap, reselct again
            if checkSlotsOverlap(self.game.player1_slots, self.game.player2_slots):
                # reset both players' slots
                print("Slots overlap!")
                self.game.player1_slots = '0,0,0'
                self.game.player2_slots = '0,0,0'
                self.game.save()

                event = {
                    'type': 'update_notification_handler',
                    'response': 'failed',
                    'message': 'Slots overlap! Please select different slots.',
                }  

            # if not overlap, start the game
            else:
                self.game.game_state = 1
                self.game.bullets_position = self.game.player1_slots + ',' + self.game.player2_slots
                self.game.current_position = random.randint(1, 24)
                self.game.bullets_remains = 6
                self.game.save()
                self.game = Game.objects.get(id=self.game_id)
                event = {
                    'type': 'update_gamePage_handler',
                    'response': 'success',
                    'message': 'Both players have selected the slots. Game starts!',
                }


        # if only one player has selected the slots
        else:
            self.game.save()
            event = {
                'type': 'update_notification_handler',
                'response': 'success',
                'message': 'One player has selected the slots.',
            }  

                    
        async_to_sync(self.channel_layer.group_send)(
            self.game_name, event
        )

    def handleShoot(self, data):
        if self.game.game_state != 1:
            return

        bullets_position = self.game.bullets_position.split(',')

        # if current position has a bullet
        if str(self.game.current_position) in bullets_position:
            self.game.bullets_remains -= 1
            # handle get shot
            if self.game.current_turn == 0:
                self.game.player1_get_shot += 1
                self.game.player1_chips -= 50
                self.game.chips_in_table += 50
                self.game.player2_chips += self.game.chips_in_table 
            else:
                self.game.player2_get_shot += 1
                self.game.player2_chips -= 50
                self.game.chips_in_table += 50
                self.game.player1_chips += self.game.chips_in_table
            
            if self.nextRound():
                return
            current_player = self.game.player1 if self.game.current_turn == 0 else self.game.player2
            event = {
                'type': 'update_gamePage_handler',
                'response': 'success',
                'message': f'{current_player} get shot!\n{current_player} lose extra 50 chips.\nNew round begins!',
                }
            
            async_to_sync(self.channel_layer.group_send)(
                self.game_name, event
            )

        # empty slot
        else:
            if self.game.current_turn == 0:
                self.game.player1_chips += self.game.chips_in_table
            else:
                self.game.player2_chips += self.game.chips_in_table
            self.game.current_turn = 1 - self.game.current_turn
            if self.nextRound():
                return
            event = {
                'type': 'update_gamePage_handler',
                'response': 'success',
                'message': 'Empty slot! New round begins!',
                }
            
            async_to_sync(self.channel_layer.group_send)(
                self.game_name, event
            )
        pass

    def handlePass(self, data):
        if self.game.game_state != 1:
            return
        # check current pass
        if self.game.current_passes >= 4:  
            bullets_position = self.game.bullets_position.split(',')

            # if current position has a bullet
            if str(self.game.current_position) in bullets_position:
                self.game.bullets_remains -= 1
                event = {
                'type': 'update_gamePage_handler',
                'response': 'success',
                'message': 'The Ref will take the shot for both players. It has a bullet! New round begins!',
                }
            else:
                event = {
                'type': 'update_gamePage_handler',
                'response': 'success',
                'message': 'The Ref will take the shot for both players. It is an empty slot! New round begins!',
                }
            # increase the round
            if self.nextRound():
                return

            async_to_sync(self.channel_layer.group_send)(
                self.game_name, event
            )

            return
        
        # if not exceed the limit, increase the pass
        self.game.current_passes += 1
        

        chips_needs_to_pay = 2 ** (self.game.current_passes-1)
        print(f"chips_needs_to_pay: {chips_needs_to_pay}")
        if self.game.current_turn == 0:
            self.game.player1_chips -= chips_needs_to_pay
            self.game.chips_in_table += chips_needs_to_pay
        else:
            self.game.player2_chips -= chips_needs_to_pay
            self.game.chips_in_table += chips_needs_to_pay


        self.game.current_turn = 1 - self.game.current_turn

        self.game.save()
        event = {
            'type': 'update_gamePage_handler',
            'response': 'success',
            'message': f'{self.user} choose to pass',
        }
        async_to_sync(self.channel_layer.group_send)(
            self.game_name, event
        )




    def nextRound(self):
        self.game.current_round += 1
        self.game.current_passes = 0
        self.game.chips_in_table = 0
        self.game.current_position = self.game.current_position % 24 + 1
        self.game.save()

        # endgame
        if self.game.current_round == 25 or self.game.bullets_remains == 0:
            # handle endgame
            self.endGame()
            return True
        return False

    def endGame(self):
        # decide the winner
        if self.game.player1_get_shot < self.game.player2_get_shot:
            winner = self.game.player1
            loser = self.game.player2
        elif self.game.player1_get_shot > self.game.player2_get_shot:
            winner = self.game.player2
            loser = self.game.player1
        else:
            if self.game.player1_chips > self.game.player2_chips:
                winner = self.game.player1
                loser = self.game.player2
            elif self.game.player1_chips < self.game.player2_chips:
                winner = self.game.player2
                loser = self.game.player1
            else:
                winner = None

        if winner:
            self.game.game_state = 2
            self.game.save()


            event = {
                'type': 'update_gamePage_handler',
                'response': 'success',
                'message': f'{winner} wins the game!',
            }

        else:
            self.game.game_state = 2
            self.game.save()
            event = {
                'type': 'update_gamePage_handler',
                'response': 'success',
                'message': 'It is a tie!',
            }
        async_to_sync(self.channel_layer.group_send)(
            self.game_name, event
        )












def validateSlots(slot1, slot2, slot3):
    if not (1 <= slot1 <= 24):
        return False
    if not (1 <= slot2 <= 24):
        return False
    if not (1 <= slot3 <= 24):
        return False
    if slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
        return False
    return True

def checkSlotsOverlap(player1_slots, player2_slots):
    player1_slots = player1_slots.split(',')
    player2_slots = player2_slots.split(',')
    for slot in player1_slots:
        if slot in player2_slots:
            return True
    return False