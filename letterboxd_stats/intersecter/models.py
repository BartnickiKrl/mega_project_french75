from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class LetterboxdUsers(models.Model):
    NickName = models.CharField(max_length=25, primary_key=True)
    MovieID = models.ManyToManyField('Movies', blank=True, related_name='users')


class Movies(models.Model):
    #movie id is created on its own
    Title = models.CharField(max_length=50)
    Year = models.IntegerField(validators=[MinValueValidator(1900),
                                           MaxValueValidator(2050)], default=1900 )
    GenreID = models.ManyToManyField('Genres', related_name='movies')
    DirectorID = models.ManyToManyField('Directors', related_name='movies')


class Genres(models.Model):
    Name = models.CharField(max_length=30, primary_key=True)

class Directors(models.Model):
    Name = models.CharField(max_length=60, primary_key=True)
