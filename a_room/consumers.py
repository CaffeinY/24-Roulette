import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import Room
from a_game.models import Game

class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.lobby_name = "lobby"
        # print(f"{self.user.username} connected")
        
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # print(f"{self.user.username} exited")

        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        
        # print(f"user:{self.user} action: {action}")

        # create room
        if action == "create-room":
            if self.user.in_room.exists():
                # print(f"{self.user.username} already in a room")
                return
                
            room = Room.objects.create(
                room_name="dummy room",
                created_by=self.user,
                is_started=False,
            )
            room.players.add(self.user)
            room.save()
            async_to_sync(self.channel_layer.group_send)(
            self.lobby_name, {
                                'type': 'new_room_handler',
                                'room_id': room.id
                             }
            )
        
        # leave room
        elif action == "exit-room":
            room_id = text_data_json['room-id']
            room = Room.objects.get(id=room_id)

            if not room.players.filter(id=self.user.id).exists():
                return 
            
            if room.is_started:
                return
            
            room.players.remove(self.user)
            room.save()

            if room.players.count() == 0:
                room.delete()
                async_to_sync(self.channel_layer.group_send)(
                self.lobby_name, {
                                    'type': 'delete_room_handler',
                                    'room_id': room_id
                                    }
                )
                
            else:
                async_to_sync(self.channel_layer.group_send)(
                self.lobby_name, {
                                    'type': 'update_room_handler',
                                    'room_id': room_id
                                    }
                )

        # join room
        elif action == "join-room":
            room_id = text_data_json['room-id']
            room = Room.objects.get(id=room_id)
            if room.players.count() == 2 or room.is_started:
                return
            
            if self.user.in_room.exists():
                # print(f"{self.user.username} already in a room")
                return

            # print(f"{self.user.username} joined room {room_id}")
            room.players.add(self.user)
            room.save()

            async_to_sync(self.channel_layer.group_send)(
            self.lobby_name, {
                                'type': 'update_room_handler',
                                'room_id': room.id
                             }
            )

        # start game
        elif action == "start-game":
            room_id = text_data_json['room-id']
            room = Room.objects.get(id=room_id)

            if room.players.count() != 2:
                return
            if room.is_started:
                return
            
            room.is_started = True
            room.save()

            # create a game
            if room.game.exists() or room.players.count() != 2:
                return
            game = Game.objects.create(
                room=room,
                player1=room.players.all()[0],
                player2=room.players.all()[1],
                player1_chips=1000,
                player2_chips=1000,
                player1_get_shot=0,
                player2_get_shot=0,
                player1_slots='0,0,0',
                player2_slots='0,0,0',
                bullets_position='0,0,0,0,0,0',
                chips_in_table=0,
                bullets_remains=0,
                current_position=0,
                current_round=1,
                current_passes=0,
                current_turn=0,
            )
            game.save()

            async_to_sync(self.channel_layer.group_send)(
            self.lobby_name, {
                                'type': 'update_room_handler',
                                'room_id': room.id
                             }
            )



        
        elif action == "delete-room":
            room_id = text_data_json['room-id']
            room = Room.objects.get(id=room_id)
            room.delete()
            async_to_sync(self.channel_layer.group_send)(
            self.lobby_name, {
                                'type': 'delete_room_handler',
                                'room_id': room_id
                             }
            )

    def new_room_handler(self, event):
        room_id = event['room_id']
        room = Room.objects.get(id=room_id)
        context = {
            'room': room,
            'room_id': room_id,
            'missing-player': 2 - room.players.count(),
            'user': self.user,
        }

        html = render_to_string('partials/room_p.html', context)
        self.send(text_data=html)
        



    def update_room_handler(self, event):
        room_id = event['room_id']
        room = Room.objects.get(id=room_id)

        context = {
            'room': room,
            'room_id': room_id,
            'missing-player': 2 - room.players.count(),
            'user': self.user,
        }

        html = render_to_string('room.html', context)
        self.send(text_data=html)


    def delete_room_handler(self, event):
        rooms = Room.objects.all()
        context = {
            'rooms': rooms,
        }
        html = render_to_string('partials/room_delete.html', context)
        self.send(text_data=html)