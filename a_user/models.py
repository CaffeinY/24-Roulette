from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static



# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name='profile')

    in_game = models.BooleanField(default=False, null=True)
    is_ready = models.BooleanField(default=False, null=True)

    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    chips = models.IntegerField(default=0)

    def __str__(self):
        return 'id=' + str(self.id) 

