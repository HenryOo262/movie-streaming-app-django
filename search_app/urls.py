
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.search_bar, name='search_app.search_bar'),
    
    path('<str:search_type>/<str:search>', views.search, name='search_app.search'),
    path('<str:content_type>/<str:search_type>/<str:search>', views.search, name='search_app.search'),
]
