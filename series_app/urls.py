from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:id>/<int:current_season>/<int:current_episode>/<str:resolution>', views.series, name='series_app.series'),
    path('<int:id>/<int:current_season>/<int:current_episode>', views.series, name='series_app.series'),
    path('<int:id>/<int:current_season>', views.series, name='series_app.series'),
    path('<int:id>', views.series, name='series_app.series'),
    path('create/', views.series_create, name='series_app.series_create'),
    path('upload/', views.series_upload, name='series_app.series_upload'),
    path('upload/<int:id>', views.series_upload, name='series_app.series_upload'),
    path('download/<str:source>', views.series_download, name='series_app.series_download'),
    path('stream/<str:source>/', views.series_stream, name='series_app.series_stream'),
]