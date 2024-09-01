
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('auth/', include('auth_app.urls')),
    path('movie/', include('movie_app.urls')),
    path('series/', include('series_app.urls')),
    path('search/', include('search_app.urls')),
    path('comments/', include('comment_app.urls')),
    path('bookmarks/', include('bookmark_app.urls')),

    path('searchTerms/', views.getSearchTerms),

    path('cast/create', views.cast_create, name='cast_create'),
    path('cast/<int:id>', views.cast, name='cast'),
]
