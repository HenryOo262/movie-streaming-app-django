from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from movie_app.models import Movie

def search(request, search_type=None, search=None):
    if search_type == 'genre':
        movies = Movie.objects.filter(genres__name__icontains=search)
    elif search_type == 'production':
        movies = Movie.objects.filter(productions__name__icontains=search)
    elif search_type == 'cast':
        movies = Movie.objects.filter(casts__name__icontains=search)
    elif search_type == 'director':
        movies = Movie.objects.filter(directors__name__icontains=search)
    elif search_type == 'rating':
        movies = Movie.objects.filter(rating=search)
    elif search_type == 'country':
        movies = Movie.objects.filter(countries__name__icontains=search)

    paginator = Paginator(movies, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }
    return render(request, 'search.html', context) 


def search_bar(request):    
    input_value = request.GET.get('input_value','')
    movies1 = Movie.objects.filter(casts__name__icontains=input_value).distinct().order_by('id')
    movies2 = Movie.objects.filter(title__icontains=input_value).distinct().order_by('id')
    movies = movies1 | movies2

    paginator = Paginator(movies, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": "resulting",
        'input_value': input_value
    }
    return render(request, 'search_bar.html', context) 