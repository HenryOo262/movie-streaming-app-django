from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/', views.bookmarks_movies, name='bookmark_app.bookmarks_movies'),
    path('series/', views.bookmarks_series, name='bookmark_app.bookmarks_series'),
    path('bookmark/movie/<int:id>', views.movie_bookmark, name='bookmark_app.movie_bookmark'),
    path('bookmark/series/<int:id>-<int:current_season>-<int:current_episode>-<str:resolution>', views.series_bookmark, name='bookmark_app.series_bookmark'),
]