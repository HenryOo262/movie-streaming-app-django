
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:search_type>/<str:search>', views.search, name='search_app.search'),
]
