# Generated by Django 5.0.6 on 2024-06-12 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_game', '0002_game_player1_is_selected_game_player2_is_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_round',
            field=models.IntegerField(default=1),
        ),
    ]
