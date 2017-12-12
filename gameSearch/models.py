from django.db import models
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL)


# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=56)
    platform = models.CharField(max_length=16)
    score = models.DecimalField(max_digits=2, decimal_places=1)
    genre = models.CharField(max_length=17)
    editors_choice = models.CharField(max_length=1)


class Favourites(models.Model):

    user = models.CharField(max_length=4)
    game = models.CharField(max_length=5)
