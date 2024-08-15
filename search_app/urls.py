
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('genre/<str:genre>', views.search_genre, name='search_app.search_genre'),
]
