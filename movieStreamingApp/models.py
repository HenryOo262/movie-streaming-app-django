from django.db import models

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

    def __str__(self):
        return self.name

