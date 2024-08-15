from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/', views.bookmark_movies, name='bookmark_app.bookmark_movies')
]