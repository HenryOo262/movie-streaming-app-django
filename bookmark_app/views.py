from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookmark
from movie_app.models import Movie
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

def bookmarks_movies(request):
    movie_bookmarks = Bookmark.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Movie))
    paginator = Paginator(movie_bookmarks, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookmark.html', {"page_obj": page_obj})   
