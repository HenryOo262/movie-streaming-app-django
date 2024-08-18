from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:id>-<str:resolution>', views.movie, name='movie_app.movie'),
    path('<int:id>', views.movie, name='movie_app.movie'),
    path('bookmark/<int:id>', views.movie_bookmark, name='movie_app.movie_bookmark'),
    path('stream/<str:source>/', views.movie_stream, name='movie_app.movie_stream'),
    path('download/<str:source>/', views.movie_download, name='movie_app.movie_download'),
    path('create/', views.movie_create, name='movie_app.movie_create'),
    path('upload/<int:id>', views.movie_upload, name='movie_app.movie_upload'),
    path('upload/', views.movie_upload, name='movie_app.movie_upload'),
]