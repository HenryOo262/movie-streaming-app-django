from django.shortcuts import render
from django.http import HttpResponse
from movie_app.models import Movie
from movieStreamingApp.models import Bookmark
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

def bookmark_movies(request):
    if request.method == 'GET':
        movie_bookmarks = Bookmark.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Movie))
        context = {
            'movie_bookmarks': movie_bookmarks
        }
        print(movie_bookmarks)
        
        return render(request, 'bookmark.html', context)   
