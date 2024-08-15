from django.http import HttpResponse
from django.shortcuts import render, redirect
from movie_app.models import Movie, MovieResource

def index(request):
    return render(request, 'index.html')

def home(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'home.html', context)  