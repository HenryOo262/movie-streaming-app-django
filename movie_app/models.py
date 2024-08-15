from django.db import models
from movieStreamingApp.models import Genre, Country

class Movie(models.Model):
    title       = models.CharField(max_length=100)
    poster      = models.CharField(max_length=255, unique=True)
    releaseDate = models.DateField()
    description = models.TextField()
    addedDateTime = models.DateTimeField(auto_now_add=True)
    genres      = models.ManyToManyField(Genre, blank=True)
    countries   = models.ManyToManyField(Country, blank=True)

    def __str__(self):
        return self.title

class MovieResource(models.Model):
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=5, choices=[('320p','320p'),('480p','480p'),('720p','720p'),('1080p','1080p')])
    source     = models.CharField(max_length=255, unique=True)

    class Meta:
        unique_together = ('movie', 'resolution')

    def __str__(self):
        return self.source