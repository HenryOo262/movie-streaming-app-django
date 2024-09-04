from firebase_admin import storage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.contenttypes.models import ContentType

from .forms import CastForm
from series_app.models import Series
from .models import Genre, Country, Cast, WatchHistory
from movie_app.models import Movie, MovieResource


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


def cast_create(request):
    if request.method == 'GET':
        form = CastForm()
        return render(request, 'cast_create.html', {'form': form})
    elif request.method == 'POST':
        form = CastForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                bio = form.cleaned_data['bio']
                image = form.cleaned_data['image']
                imdb = form.cleaned_data['imdb']

                if image:
                    bucket = storage.bucket()
                    # creates a reference in bucket
                    blob = bucket.blob(f'casts/{image.name}')
                    blob.upload_from_file(image)
                    blob.make_public()  
                    image_url = blob.public_url 

                cast_object, created = Cast.objects.get_or_create(name=name)
                cast_object.bio = bio if bio else cast_object.bio
                cast_object.image = image_url if image else cast_object.image
                cast_object.imdb = imdb if imdb else cast_object.imdb
                cast_object.save()

                if created:
                    messages.success(request, 'Successfully created the cast')
                else:
                    messages.success(request, 'Successfully updated the cast')
                return render(request, 'cast_create.html', {'form': form})
            except Exception as e:
                raise e
        return render(request, 'cast_create.html', {'form': form})
    

def cast(request, id):
    try:
        cast = Cast.objects.get(id=id)
        movies = Movie.objects.filter(casts__id=id)[:5]
        series = Series.objects.filter(casts__id=id)[:5]
        context = {
            'cast': cast,
            'movies': movies,
            'series': series,
        }
    except Exception as e:
        raise e
    return render(request, 'cast.html', context)


@login_required
def watchHistory(request, content_type):
    """ Returns Paginated Pages of Watched History movies """
    if content_type == 'movies':
        model = Movie
    elif content_type == 'series':
        model = Series

    watch_history = WatchHistory.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(model)).order_by('-addedDateTime')
    paginator = Paginator(watch_history, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj, 
        "content_type": content_type,
    } 
    return render(request, 'watch_history.html', context) 