from django.db import models
from movieStreamingApp.models import Genre, Country, Production, Director, Cast

class Series(models.Model):
    title       = models.CharField(max_length=255)
    poster      = models.CharField(max_length=255, unique=True)
    releaseDate = models.DateField()
    description = models.TextField()
    status      = models.CharField(max_length=10, choices=[('Ongoing','Ongoing'),('Completed','Completed'),('Hiatus','Hiatus'),('Canceled','Canceled')])
    rating      = models.CharField(max_length=5, choices=[('G','G'),('PG','PG'),('PG-13','PG-13'),('R','R'),('NC-17','NC-17')])
    addedDateTime = models.DateTimeField(auto_now_add=True)
    genres      = models.ManyToManyField(Genre, blank=True)
    countries   = models.ManyToManyField(Country, blank=True)
    productions = models.ManyToManyField(Production, blank=True, null=True)
    directors   = models.ManyToManyField(Director, blank=True, null=True)
    casts       = models.ManyToManyField(Cast, blank=True, null=True)
    views       = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class Season(models.Model):
    series = models.ForeignKey(Series, blank=True, on_delete=models.CASCADE)
    season = models.PositiveIntegerField()

    def __str__(self):
        return self.series.title + '-' + str(self.season)
    

class Episode(models.Model):
    season = models.ForeignKey(Season, blank=True, on_delete=models.CASCADE)
    episode = models.PositiveBigIntegerField()

    def __str__(self):
        return self.season.series.title + '-' + str(self.season.season) + '-' + str(self.episode)


class SeriesResource(models.Model):
    episode    = models.ForeignKey(Episode, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=5, choices=[('320p','320p'),('480p','480p'),('720p','720p'),('1080p','1080p')])
    source     = models.CharField(max_length=255, unique=True)

    class Meta:
        unique_together = ('episode', 'resolution')

    def __str__(self):
        return self.source
