from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText   = models.TextField()
    addedDateTime = models.DateTimeField(auto_now_add=True)
    content_type  = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id     = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.commentText
    
class Bookmark(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    addedDateTime = models.DateTimeField(auto_now_add=True)
    content_type  = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id     = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')