from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/', views.bookmarks_movies, name='bookmark_app.bookmarks_movies')
]