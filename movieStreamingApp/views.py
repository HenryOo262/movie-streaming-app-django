from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import Genre, Country
from movie_app.models import Movie
from series_app.models import Series


def index(request):
    return render(request, 'index.html')


def home(request):
    movies = Movie.objects.all().order_by('-releaseDate')[:12]
    series = Series.objects.all().order_by('-releaseDate')[:12]
    context = {
        'movies': movies,
        'series': series,
    }
    return render(request, 'home.html', context)  


def getSearchTerms(request):
    genres = list(Genre.objects.all().order_by('name').values_list('name', flat=True))
    countries = list(Country.objects.all().order_by('name').values_list('name', flat=True))

    data = {
        'genres': genres,
        'countries': countries,
    }
    return JsonResponse(data)