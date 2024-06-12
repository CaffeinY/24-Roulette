# Generated by Django 5.0.6 on 2024-06-10 23:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_room', '0003_room_pictureurl'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='players',
            field=models.ManyToManyField(default=None, related_name='in_room', to=settings.AUTH_USER_MODEL),
        ),
    ]
