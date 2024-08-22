import re
from pathlib import Path
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, StreamingHttpResponse
from firebase_admin import storage, initialize_app, credentials
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from utils.custom_decorators import superuser_required

from . import forms
from comment_app.models import Comment
from bookmark_app.models import Bookmark
from comment_app.forms import CommentForm, EditForm
from .models import Series, Season, SeriesResource, Episode
from movieStreamingApp.models import Cast, Production, Director


def file_iterator(blob, start, end):
    try:
        chunk = blob.download_as_bytes(start=start, end=end)
        # print(len(chunk))
        yield chunk
    except Exception as e:
        print(f"Error downloading file chunk: {e}")
        raise


def series(request, id, current_season=None, current_episode=None, resolution=None):
    """ Send Series Information """
    if request.method == 'GET':
        current_season  = 1 if current_season==None else current_season
        current_episode = 1 if current_episode==None else current_episode

        try:
            series = Series.objects.get(id=id)

            seasons = series.season_set.values('season').order_by('season')
            current_season = series.season_set.get(season=current_season)

            episodes = current_season.episode_set.values('episode').order_by('episode')
            current_episode = current_season.episode_set.get(episode=current_episode)

            resolutions = current_episode.seriesresource_set.values('resolution')

            comment_form = CommentForm()
            edit_form = EditForm()

            '''
            comments      = Comment.objects.filter(object_id=current_episode.id, content_type=ContentType.objects.get_for_model(Episode)).order_by('-addedDateTime')
            paginator     = Paginator(comments, 5)
            page_number   = request.GET.get("page")
            page_obj      = paginator.get_page(page_number)
            '''

            genres = series.genres.filter()
            countries = series.countries.filter()
            productions = series.productions.filter()
            directors = series.directors.filter()
            casts = series.casts.filter()

            series.views = series.views + 1
            series.save()

            if request.user.is_authenticated:
                bookmarks = Bookmark.objects.filter(user=request.user, object_id=id, content_type=ContentType.objects.get_for_model(Series))
                if bookmarks.exists():
                    bookmarked = True
                else:
                    bookmarked = False
            else:
                bookmarked = False

            if resolution == None:
                series_resource = current_episode.seriesresource_set.first() 
            else:
                series_resource = current_episode.seriesresource_set.get(resolution=resolution)
            
            context = {
                'series': series,
                'seasons': seasons,
                'episodes': episodes,
                'current_season': current_season,
                'current_episode': current_episode,
                'series_resource': series_resource,
                'resolutions': resolutions,
                'comment_form': comment_form,
                'edit_form': edit_form,
                'genres': genres,
                'countries': countries,
                'productions': productions,
                'directors': directors,
                'casts': casts,
                'bookmarked': bookmarked,
                'content_type':'series',
            }
            return render(request, 'series.html', context)
        
        except Exception as e:
            raise e


def series_stream(request, source):
    # Retrieve the file name from storage 
    file = storage.bucket().blob(f'series/{source}')
    file.reload()  
    file_size = file.size

    # Get the range header
    range = request.headers.get('Range', None)
    if not range:
        return HttpResponse(status=416)
    
    # Parse the range header
    byte_range = re.search(r'bytes=(\d+)-(\d*)', range).groups()
    start = int(byte_range[0])
    end = min(start + 1000000, file_size - 1)
   
    # Create the response
    response = StreamingHttpResponse(file_iterator(file, start, end), status=206)
    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = end - start + 1
    response['Content-Type'] = 'video/mp4'

    return response 
        

@superuser_required
def series_create(request):
    """ Send the series create form and process data """
    if request.method == 'GET':
        series_form = forms.SeriesForm()
        productions = Production.objects.filter()
        directors = Director.objects.filter()
        casts = Cast.objects.filter()
        context = {
            'form': series_form,
            'productions': productions,
            'directors': directors,
            'casts': casts,
        }
        return render(request, 'series_create.html', context)
    
    elif request.method == 'POST':
        series_form = forms.SeriesForm(request.POST, request.FILES)
        if series_form.is_valid():

            try:
                title         = series_form.cleaned_data['title']
                releaseDate   = series_form.cleaned_data['releaseDate']
                description   = series_form.cleaned_data['description']
                genres        = series_form.cleaned_data['genre']
                countries     = series_form.cleaned_data['country']
                poster        = series_form.cleaned_data['poster']
                rating        = series_form.cleaned_data['rating']
                production    = series_form.cleaned_data['production']
                coproduction1 = series_form.cleaned_data['coproduction1']
                coproduction2 = series_form.cleaned_data['coproduction2']
                director      = series_form.cleaned_data['director']
                codirector    = series_form.cleaned_data['codirector']
                cast          = series_form.cleaned_data['cast']
                cocast1       = series_form.cleaned_data['cocast1']
                cocast2       = series_form.cleaned_data['cocast2']

                bucket = storage.bucket()
                blob = bucket.blob(f'posters/{poster.name}')
                blob.upload_from_file(poster)
                blob.make_public()  
                poster_url = blob.public_url

                new_series = Series(title=title, rating=rating, poster=poster_url, releaseDate=releaseDate, description=description)
                new_series.save()
                new_series.genres.set(genres)
                new_series.countries.set(countries)

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
                new_series.productions.set(productions)

                directors = []
                if director != '':
                    director, created = Director.objects.get_or_create(name=director)
                    directors.append(director)
                if codirector != '':
                    codirector, created = Director.objects.get_or_create(name=codirector)
                    directors.append(codirector)
                new_series.directors.set(directors)

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
                new_series.casts.set(casts)

                messages.success(request, 'Series has been succesfully created')
                return redirect('series_app.series_upload', id=new_series.id)
            
            except Exception as e:
                raise e
        
        return render(request, 'series_create.html', {'form': series_form})
            

@superuser_required
def series_upload(request, id=None):
    """ Before uploading to firebase, save metadata to DB """
    if request.method == 'GET':
        series = Series.objects.get(id=id)
        seriesResource_form = forms.SeriesResourceForm(initial={'series':id})
        context = {
            'series': series,
            'form': seriesResource_form
        }
        return render(request, 'series_upload.html', context)
    
    elif request.method == 'POST':
        seriesResource_form = forms.SeriesResourceForm(request.POST, request.FILES) 
        if seriesResource_form.is_valid():

            try:
                resolution = seriesResource_form.cleaned_data['resolution']
                source = seriesResource_form.cleaned_data['sourceFileName']
                series = seriesResource_form.cleaned_data['series']
                season = seriesResource_form.cleaned_data['season']
                episode = seriesResource_form.cleaned_data['episode']

                # series, season, episode are integers (id)
                target_series = Series.objects.get(id=series)
                target_season, created = Season.objects.get_or_create(series=target_series, season=season)
                target_episode, created = Episode.objects.get_or_create(season=target_season, episode=episode)

                new_seriesResource = SeriesResource(episode=target_episode, resolution=resolution, source=source)
                new_seriesResource.save()
                return HttpResponse(status = 200) 
            
            except IntegrityError as i:
                raise i
                return HttpResponse(status = 500)
            
            except Exception as e:
                raise e
                return HttpResponse(status = 500)
    
        return render(request, 'series_upload.html', {'form': seriesResource_form})


@login_required
def series_download(request, source):
    """ Get a signed url of the video file """
    try:
        expiration = datetime.now() + timedelta(minutes=5)
        download_url = storage.bucket().blob(f'series/{source}').generate_signed_url(expiration=expiration)
        return render(request, 'movie_download.html', {'download_url':download_url})
    
    except Exception as e:
        raise e