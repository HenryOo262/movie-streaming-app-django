from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Genre(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name
    

class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    

class Production(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Director(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Cast(models.Model):    
    name = models.CharField(max_length=255, unique=True)
    bio  = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, unique=True, null=True, blank=True)
    imdb = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class WatchHistory(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    addedDateTime = models.DateTimeField(auto_now_add=True)
    content_type  = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id     = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')