from django.db import models
from django.contrib.auth.models import User
from a_room.models import Room


# Create your models here.
class Game(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='game')

    # Game state
    # 0: Selecting slots 
    game_state = models.IntegerField(default=0)

    # Player 1 and Player 2
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2')
    player1_chips = models.IntegerField(default=0)
    player2_chips = models.IntegerField(default=0)
    player1_get_shot = models.IntegerField(default=0)
    player2_get_shot = models.IntegerField(default=0)

    # bullets
    player1_slots = models.CharField(max_length=255, default='0,0,0')
    player2_slots = models.CharField(max_length=255, default='0,0,0')
    player1_is_selected = models.BooleanField(default=False)
    player2_is_selected = models.BooleanField(default=False)

    # bullets position
    bullets_position = models.CharField(max_length=255, default='0,0,0,0,0,0')
    

    # game variable
    chips_in_table = models.IntegerField(default=0)
    bullets_remains = models.IntegerField(default=0)

     
    current_position = models.IntegerField(default=0)
    current_round = models.IntegerField(default=1)
    current_passes = models.IntegerField(default=0)


    # 0: Player 1's turn        1: Player 2's turn
    current_turn = models.IntegerField(default=0)
    



    def __str__(self):
        return f"{self.id}"