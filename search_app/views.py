from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from movie_app.models import Movie
from series_app.models import Series


def search(request, content_type=None, search_type=None, search=None):
    """ Search Movies or Series via Navbar ModalBox """
    if content_type is None:
        content_type = 'movies'

    if content_type == 'movies':
        model = Movie
    elif content_type == 'series':
        model = Series

    searchTypeInvalidForMovie = False

    try:
        if search_type == 'genre':
            content = model.objects.filter(genres__name__icontains=search)
        elif search_type == 'production':
            content = model.objects.filter(productions__name__icontains=search)
        elif search_type == 'cast':
            content = model.objects.filter(casts__name__icontains=search)
        elif search_type == 'director':
            content = model.objects.filter(directors__name__icontains=search)
        elif search_type == 'rating':
            content = model.objects.filter(rating=search)
        elif search_type == 'status':
            content = model.objects.filter(status=search)
            searchTypeInvalidForMovie = True
        elif search_type == 'country':
            content = model.objects.filter(countries__name__icontains=search)
    except Exception as e:
        return HttpResponse(e)

    paginator = Paginator(content, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "content_type": content_type,
        "search_type": search_type,
        "search": search,
        "searchTypeInvalidForMovie": searchTypeInvalidForMovie,
    }
    return render(request, 'search.html', context) 


def search_bar(request, content_type=None):    
    """ Search Movies or Series via SearchBar """
    content_type = request.GET.get('content_type','movies')

    if content_type == 'movies':
        model = Movie
    elif content_type == 'series':
        model = Series

    input_value = request.GET.get('input_value','')
    content1 = model.objects.filter(casts__name__icontains=input_value).distinct().order_by('id')
    content2 = model.objects.filter(title__icontains=input_value).distinct().order_by('id')
    content = content1 | content2

    paginator = Paginator(content, 12)

    # If page_number is null, page_obj is for the first page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": "resulting",
        "content_type": content_type,
        "input_value": input_value,
    }
    return render(request, 'search_bar.html', context) 