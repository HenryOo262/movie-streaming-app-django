from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

from .models import Bookmark
from movie_app.models import Movie
from series_app.models import Series


def bookmarks_movies(request):
    """ Returns Paginated Pages of Bookmarked movies """
    movie_bookmarks = Bookmark.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Movie))
    paginator = Paginator(movie_bookmarks, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookmark.html', {"page_obj": page_obj, "content_type": "movies"})   


def bookmarks_series(request):
    """ Returns Paginated Pages of Bookmarked series """
    series_bookmarks = Bookmark.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Series))
    paginator = Paginator(series_bookmarks, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookmark.html', {"page_obj": page_obj, "content_type": "series"})   


def movie_bookmark(request, id):
    """ Bookmark the movie if its id exists in Bookmark table, else delete the record """
    if request.method == 'POST':
        bookmark = Bookmark.objects.filter(user=request.user, object_id=id, content_type=ContentType.objects.get_for_model(Movie))
        if bookmark.exists():
            bookmark.delete()
            return redirect('movie_app.movie', id=id)
        else:
            new_bookmark = Bookmark(user=request.user, content_type=ContentType.objects.get_for_model(Movie), object_id=id)
            new_bookmark.save()
            return redirect('movie_app.movie', id=id)
        

def series_bookmark(request, id, current_season, current_episode, resolution):
    """ Bookmark the series if its id exists in Bookmark table, else delete the record """
    if request.method == 'POST':
        bookmark = Bookmark.objects.filter(user=request.user, object_id=id, content_type=ContentType.objects.get_for_model(Series))
        if bookmark.exists():
            bookmark.delete()
            return redirect('series_app.series', id=id, current_season=current_season, current_episode=current_episode, resolution=resolution)
        else:
            new_bookmark = Bookmark(user=request.user, content_type=ContentType.objects.get_for_model(Series), object_id=id)
            new_bookmark.save()
            return redirect('series_app.series', id=id, current_season=current_season, current_episode=current_episode, resolution=resolution)
        