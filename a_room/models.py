from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)
    # password = models.CharField(max_length=10)
    players = models.ManyToManyField(User, default=None, related_name="in_room")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, default=None, on_delete=models.PROTECT)

    is_started = models.BooleanField(default=False)

    pictureURL = models.URLField(max_length=200, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXV1enkTapX92ottfs5NAiaMqI66nB_NV_KA&s") 

    def __str__(self):
        return self.room_name