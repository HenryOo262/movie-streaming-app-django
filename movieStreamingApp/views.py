from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import Genre, Country
from movie_app.models import Movie, MovieResource
from series_app.models import Series


def index(request):
    return render(request, 'index.html')


def home(request):
    latest_movies = Movie.objects.filter(movieresource__isnull=False).distinct().order_by('-releaseDate')[:6]
    latest_series = Series.objects.filter(season__isnull=False).distinct().order_by('-releaseDate')[:6]
    mostviewed_movies = Movie.objects.filter(movieresource__isnull=False).distinct().order_by('-views')[:3]
    mostviewed_series = Series.objects.filter(season__isnull=False).distinct().order_by('-views')[:3]
    ongoing_series = Series.objects.filter(season__isnull=False, status='Ongoing').distinct()[:6]

    context = {
        'latest_movies': latest_movies,
        'latest_series': latest_series,
        'mostviewed_movies': mostviewed_movies,
        'mostviewed_series': mostviewed_series,
        'ongoing_series': ongoing_series,
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