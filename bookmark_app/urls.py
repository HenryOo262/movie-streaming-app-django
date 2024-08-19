from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:content_type>/', views.bookmarks, name='bookmark_app.bookmarks'),
    path('bookmark/movie/<int:id>', views.movie_bookmark, name='bookmark_app.movie_bookmark'),
    path('bookmark/series/<int:id>/<int:current_season>/<int:current_episode>/<str:resolution>', views.series_bookmark, name='bookmark_app.series_bookmark'),
]