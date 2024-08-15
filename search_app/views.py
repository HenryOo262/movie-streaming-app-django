from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from movie_app.models import Movie

def search_genre(request):

    return render(request, 'result.html', context)