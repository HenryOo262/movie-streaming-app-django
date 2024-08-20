from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType

from .models import Bookmark
from movie_app.models import Movie
from series_app.models import Series


def bookmarks(request, content_type):
    """ Returns Paginated Pages of Bookmarked movies """
    if content_type == 'movies':
        model = Movie
    elif content_type == 'series':
        model = Series

    bookmarks = Bookmark.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(model))
    paginator = Paginator(bookmarks, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj, 
        "content_type": content_type,
    } 
    return render(request, 'bookmark.html', context)   


def movie_bookmark(request, id):
    """ Bookmark the movie if its id exists in Bookmark table, else delete the record """
    if request.method == 'POST':
        bookmark = Bookmark.objects.filter(user=request.user, object_id=id, content_type=ContentType.objects.get_for_model(Movie))
        if bookmark.exists():
            bookmark.delete()
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
        else:
            new_bookmark = Bookmark(user=request.user, content_type=ContentType.objects.get_for_model(Series), object_id=id)
            new_bookmark.save()
    return redirect('series_app.series', id=id, current_season=current_season, current_episode=current_episode, resolution=resolution)
        