import os
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from firebase_admin import storage, initialize_app, credentials
from . import forms
from .models import MovieResource, Movie
from movieStreamingApp.forms import CommentForm
from movieStreamingApp.models import Comment, Production, Director, Cast
from bookmark_app.models import Bookmark
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
serviceAccount = os.path.join(BASE_DIR, 'firebase', './video-stream-app-6b509-firebase-adminsdk-f62d7-0d43816024.json')
cred = credentials.Certificate(serviceAccount)
buck = 'video-stream-app-6b509.appspot.com'

initialize_app(cred, 
    {'storageBucket': buck}
)


#######################################################################


def file_iterator(blob, start, end):
    try:
        # Download chunk directly as bytes
        chunk = blob.download_as_bytes(start=start, end=end)
        print(len(chunk))
        yield chunk
    except Exception as e:
        print(f"Error downloading file chunk: {e}")
        raise


#######################################################################


def get_sources(x):
    sources = []
    for i in x:
        sources.append(i.source)
    return sources

def get_resolutions(x):
    resolutions = []
    for i in x:
        resolutions.append(i.resolution)
    return resolutions


#######################################################################

def movie(request, id, resolution=None):
    if request.method == 'GET':
        try:
            comment_form = CommentForm()
            movie = Movie.objects.get(id=id)
            resolutions = movie.movieresource_set.values('resolution')
            genres = movie.genres.filter()
            countries = movie.countries.filter()
            productions = movie.productions.filter()
            directors = movie.directors.filter()
            casts = movie.casts.filter()
            comments = Comment.objects.filter(object_id=id, content_type=ContentType.objects.get_for_model(Movie)).order_by('-addedDateTime')

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
            else:
                movie_resource = movie.movieresource_set.get(resolution=resolution)
            
            context = {
                'movie': movie,
                'movie_resource': movie_resource,
                'resolutions': resolutions,
                'genres': genres,
                'countries': countries,
                'comments': comments,
                'productions': productions,
                'directors': directors,
                'casts': casts,
                'comment_form': comment_form,
                'bookmarked': bookmarked,
            }
            return render(request, 'movie.html', context)
        except Exception as e:
            print(e)
            return render(request, '404.html')
    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            commentText = comment_form.cleaned_data['commentText']
            new_comment = Comment(user=request.user, commentText=commentText, content_type=ContentType.objects.get_for_model(Movie), object_id=id)
            new_comment.save()
            return redirect('movie_app.movie', id=id)


def movie_bookmark(request, id):
    if request.method == 'POST':
        bookmark = Bookmark.objects.filter(user=request.user, object_id=id, content_type=ContentType.objects.get_for_model(Movie))
        if bookmark.exists():
            bookmark.delete()
            return redirect('movie_app.movie', id=id)
        else:
            new_bookmark = Bookmark(user=request.user, content_type=ContentType.objects.get_for_model(Movie), object_id=id)
            new_bookmark.save()
            return redirect('movie_app.movie', id=id)


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


def movie_download(request, source):
    expiration = datetime.now() + timedelta(minutes=5)
    download_url = storage.bucket().blob(f'movies/{source}').generate_signed_url(expiration=expiration)
    return render(request, 'movie_download.html', {'download_url':download_url})


def movie_create(request):
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
                title = movie_form.cleaned_data['title']
                releaseDate = movie_form.cleaned_data['releaseDate']
                description = movie_form.cleaned_data['description']
                genres = movie_form.cleaned_data['genre']
                countries = movie_form.cleaned_data['country']
                poster = movie_form.cleaned_data['poster']
                rating = movie_form.cleaned_data['rating']
                production = movie_form.cleaned_data['production']
                coproduction1 = movie_form.cleaned_data['coproduction1']
                coproduction2 = movie_form.cleaned_data['coproduction2']
                director = movie_form.cleaned_data['director']
                codirector = movie_form.cleaned_data['codirector']
                cast = movie_form.cleaned_data['cast']
                cocast1 = movie_form.cleaned_data['cocast1']
                cocast2 = movie_form.cleaned_data['cocast2']

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
                if not production is '':
                    production, created = Production.objects.get_or_create(name=production)
                    productions.append(production)
                if not coproduction1 is '':
                    coproduction1, created = Production.objects.get_or_create(name=coproduction1)
                    productions.append(coproduction1)
                if not coproduction2 is '':
                    coproduction2, created = Production.objects.get_or_create(name=coproduction2)
                    productions.append(coproduction2)
                new_movie.productions.set(productions)

                # handle directors
                directors = []
                if not director is '':
                    director, created = Director.objects.get_or_create(name=director)
                    directors.append(director)
                if not codirector is '':
                    codirector, created = Director.objects.get_or_create(name=codirector)
                    directors.append(codirector)
                new_movie.directors.set(directors)

                # handle casts
                casts = []
                if not cast is '':
                    cast, created = Cast.objects.get_or_create(name=cast)
                    casts.append(cast)
                if not cocast1 is '':
                    cocast1, created = Cast.objects.get_or_create(name=cocast1)
                    casts.append(cocast1)
                if not cocast2 is '':
                    cocast2, created = Cast.objects.get_or_create(name=cocast2)
                    casts.append(cocast2)
                new_movie.casts.set(casts)

                messages.success(request, 'Movie has been succesfully created')
                return redirect('movie_app.movie_upload', id=new_movie.id)
            except Exception as e:
                print(e)
                messages.error(request, 'An error has occured while creating the movie')
                return render(request, 'movie_create.html', {'form': movie_form})
        else:
            return render(request, 'movie_create.html', {'form': movie_form})
            

def movie_upload(request, id=None):
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
                resolution = movieResource_form.cleaned_data['resolution']
                source = movieResource_form.cleaned_data['sourceFileName']
                movie = movieResource_form.cleaned_data['movie']
                new_movieResource = MovieResource(movie=movie,resolution=resolution,source=source)
                new_movieResource.save()
                return HttpResponse(status = 200) 
            except IntegrityError:
                print(IntegrityError)
                return HttpResponse(status = 500)
            except Exception:
                print(Exception)
                return HttpResponse(status = 500)
        else:
            return render(request, 'movie_upload.html', {'form':movieResource_form})