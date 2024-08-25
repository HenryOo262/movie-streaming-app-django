import re
from firebase_admin import storage
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from utils.custom_decorators import superuser_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from utils.file_iterator import file_iterator

from . import forms
from comment_app.models import Comment
from .models import MovieResource, Movie
from bookmark_app.models import Bookmark
from comment_app.forms import CommentForm, EditForm
from movieStreamingApp.models import Production, Director, Cast


def movie(request, id, resolution=None):
    """ Send Movie Information """
    if request.method == 'GET':

        try:
            comment_form  = CommentForm()
            edit_form     = EditForm()
            movie         = Movie.objects.get(id=id)
            resolutions   = movie.movieresource_set.values('resolution')
            genres        = movie.genres.filter()
            countries     = movie.countries.filter()
            productions   = movie.productions.filter()
            directors     = movie.directors.filter()
            casts         = movie.casts.filter()

            movie.views = movie.views + 1
            movie.save()

            if request.user.is_authenticated:
                bookmarks = Bookmark.objects.filter(user=request.user, object_id=id, content_type=ContentType.objects.get_for_model(Movie))
                if bookmarks.exists():
                    bookmarked = True
                else:
                    bookmarked = False
            else:
                bookmarked = False

            if resolution == None:
                movie_resource = movie.movieresource_set.first() 
                if(movie_resource is None and request.user.is_superuser):
                    return redirect('movie_app.movie_upload', id=id)
            else:
                movie_resource = movie.movieresource_set.get(resolution=resolution)
            
            context = {
                'movie': movie,
                'movie_resource': movie_resource,
                'resolutions': resolutions,
                'genres': genres,
                'countries': countries,
                'productions': productions,
                'directors': directors,
                'casts': casts,
                'comment_form': comment_form,
                'edit_form': edit_form,
                'bookmarked': bookmarked,
                'content_type':'movies',
            }
            return render(request, 'movie.html', context)

        except Exception as e:
            raise e


def movie_stream(request, source):
    # access file from fire storage
    file = storage.bucket().blob(f'movies/{source}')
    file.reload()  
    file_size = file.size

    # get range from user ( initial is 0- )
    range = request.headers.get('Range', None)
    if not range:
        return HttpResponse(status=416)
    
    # split x and y from range: x - y
    byte_range = re.search(r'bytes=(\d+)-(\d*)', range).groups()
    start = int(byte_range[0])

    # 1000Bytes is 0 - 999 just like array, 
    # thus end is either start + chunk or file_size - 1, whichever smaller
    # file_size - 1 to make sure there is no out of bound
    end = min(start + 1000000, file_size - 1)
   
    response = StreamingHttpResponse(file_iterator(file, start, end), status=206)
    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = end - start + 1
    response['Content-Type'] = 'video/mp4'

    return response 


@login_required
def movie_download(request, source):
    expiration = datetime.now() + timedelta(minutes=5)
    download_url = storage.bucket().blob(f'movies/{source}').generate_signed_url(expiration=expiration)
    return render(request, 'movie_download.html', {'download_url':download_url})


@superuser_required
def movie_create(request):
    """ Send the movie create form and Process Data """
    if request.method == 'GET':
        movie_form = forms.MovieForm()
        productions = Production.objects.filter()
        directors = Director.objects.filter()
        casts = Cast.objects.filter()
        context = {
            'form': movie_form,
            'productions': productions,
            'directors': directors,
            'casts': casts,
        }
        return render(request, 'movie_create.html', context)
    
    elif request.method == 'POST':
        movie_form = forms.MovieForm(request.POST,request.FILES)

        if movie_form.is_valid():
            try:
                title        = movie_form.cleaned_data['title']
                releaseDate  = movie_form.cleaned_data['releaseDate']
                description  = movie_form.cleaned_data['description']
                genres       = movie_form.cleaned_data['genre']
                countries    = movie_form.cleaned_data['country']
                poster       = movie_form.cleaned_data['poster']
                rating       = movie_form.cleaned_data['rating']
                production    = movie_form.cleaned_data['production']
                coproduction1 = movie_form.cleaned_data['coproduction1']
                coproduction2 = movie_form.cleaned_data['coproduction2']
                director      = movie_form.cleaned_data['director']
                codirector    = movie_form.cleaned_data['codirector']
                cast          = movie_form.cleaned_data['cast']
                cocast1       = movie_form.cleaned_data['cocast1']
                cocast2       = movie_form.cleaned_data['cocast2']

                bucket = storage.bucket()
                # creates a reference in bucket
                blob = bucket.blob(f'posters/{poster.name}')
                blob.upload_from_file(poster)
                blob.make_public()  
                poster_url = blob.public_url

                new_movie = Movie(title=title, rating=rating, poster=poster_url, releaseDate=releaseDate, description=description)
                new_movie.save()
                new_movie.genres.set(genres)
                new_movie.countries.set(countries)

                # handle productions
                productions = []
                if production != '':
                    production, created = Production.objects.get_or_create(name=production)
                    productions.append(production)
                if coproduction1 != '':
                    coproduction1, created = Production.objects.get_or_create(name=coproduction1)
                    productions.append(coproduction1)
                if coproduction2 != '':
                    coproduction2, created = Production.objects.get_or_create(name=coproduction2)
                    productions.append(coproduction2)
                new_movie.productions.set(productions)

                # handle directors
                directors = []
                if director != '':
                    director, created = Director.objects.get_or_create(name=director)
                    directors.append(director)
                if codirector != '':
                    codirector, created = Director.objects.get_or_create(name=codirector)
                    directors.append(codirector)
                new_movie.directors.set(directors)

                # handle casts
                casts = []
                if cast != '':
                    cast, created = Cast.objects.get_or_create(name=cast)
                    casts.append(cast)
                if cocast1 != '':
                    cocast1, created = Cast.objects.get_or_create(name=cocast1)
                    casts.append(cocast1)
                if cocast2 != '':
                    cocast2, created = Cast.objects.get_or_create(name=cocast2)
                    casts.append(cocast2)
                new_movie.casts.set(casts)

                messages.success(request, 'Movie has been succesfully created')
                return redirect('movie_app.movie_upload', id=new_movie.id)
            
            except Exception as e:
                raise e
            
        return render(request, 'movie_create.html', {'form': movie_form})
            

@superuser_required
def movie_upload(request, id=None):
    """ Before uploading to firebase, save metadata to DB """
    if request.method == 'GET':
        movie = Movie.objects.get(id=id)
        movieResource_form = forms.MovieResourceForm(initial={'movie':movie})
        context = {
            'movie': movie,
            'form': movieResource_form
        }
        return render(request, 'movie_upload.html', context)
    
    elif request.method == 'POST':
        movieResource_form = forms.MovieResourceForm(request.POST, request.FILES) 
        if movieResource_form.is_valid():
            
            try:
                resolution  = movieResource_form.cleaned_data['resolution']
                source      = movieResource_form.cleaned_data['sourceFileName']
                movie       = movieResource_form.cleaned_data['movie']

                new_movieResource = MovieResource(movie=movie,resolution=resolution,source=source)
                new_movieResource.save()
                return HttpResponse(status = 200) 
            
            except IntegrityError as i:
                raise i
                return HttpResponse(status = 500)
            
            except Exception as e:
                raise e
                return HttpResponse(status = 500)
            
        return render(request, 'movie_upload.html', {'form':movieResource_form})