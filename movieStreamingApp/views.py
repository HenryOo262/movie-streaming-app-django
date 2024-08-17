from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from movie_app.models import Movie, MovieResource
from .models import Genre, Country
from django.urls import reverse

def index(request):
    return render(request, 'index.html')


def home(request):
    movies = Movie.objects.all()[:12]
    context = {
        'movies': movies,
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