
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('<int:comment_id>/delete/', views.delete_comment, name='comment_app.delete_comment'),

    path('<str:content_type>/<int:id>/create/', views.create_comment, name='comment_app.create_comment'),
    path('<str:content_type>/<int:id>/<int:season>/<int:episode>/create/', views.create_comment, name='comment_app.create_comment'),

    path('edit/', views.edit_comment, name='comment_app.edit_comment'),

    path('<str:content_type>/<int:id>/load/', views.load_comment, name='comment_app.load_comment'),
    path('<str:content_type>/<int:id>/<int:season>/<int:episode>/load/', views.load_comment, name='comment_app.load_comment'),
]


"""
urlpatterns = [
    path('<str:content_type>/<int:id>/<str:resolution>/<int:comment_id>/delete/', views.delete_comment, name='comment_app.delete_comment'),
    path('<str:content_type>/<int:id>/<int:season>/<int:episode>/<str:resolution>/<int:comment_id>/delete/', views.delete_comment, name='comment_app.delete_comment'),

    path('<str:content_type>/<int:id>/<str:resolution>/create/', views.create_comment, name='comment_app.create_comment'),
    path('<str:content_type>/<int:id>/<int:season>/<int:episode>/<str:resolution>/create/', views.create_comment, name='comment_app.create_comment'),

    path('<str:content_type>/<int:id>/<str:resolution>/edit/', views.edit_comment, name='comment_app.edit_comment'),
    path('<str:content_type>/<int:id>/<int:season>/<int:episode>/<str:resolution>/edit/', views.edit_comment, name='comment_app.edit_comment'),
]
"""
