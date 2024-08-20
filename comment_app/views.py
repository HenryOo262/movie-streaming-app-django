from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType

from .models import Comment
from movie_app.models import Movie
from .forms import CommentForm, EditForm
from series_app.models import Series, Episode, Season


def redirect_data(content_type, id, resolution, season=None, episode=None):
    """ Returns The Redirect URL And URL Params """
    if content_type == 'movies':
            redirect_url = 'movie_app.movie'
            redirect_kwargs = {
                'id': id,
                'resolution': resolution,
            }
    elif content_type == 'series':
        redirect_url = 'series_app.series'
        redirect_kwargs = {
            'id': id,
            'resolution': resolution,
            'current_season': season,
            'current_episode': episode,
        }
    return (redirect_url, redirect_kwargs)


def create_comment(request, content_type, id, resolution, season=None, episode=None):
    """ Add New Comments To The Comment Table """
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        # Data To Redirect
        redirect_url, redirect_kwargs = redirect_data(id=id, content_type=content_type, resolution=resolution, season=season, episode=episode)

        # If Valid
        if comment_form.is_valid():
            commentText = comment_form.cleaned_data.get('commentText')
            if content_type == 'movies':
                new_comment  = Comment(user=request.user, object_id=id, commentText=commentText, content_type=ContentType.objects.get_for_model(Movie))
            elif content_type == 'series':
                target_series = Series.objects.get(id=id)
                target_season = target_series.season_set.get(season=season) 
                target_episode = target_season.episode_set.get(episode=episode)
                new_comment  = Comment(user=request.user, object_id=target_episode.id, commentText=commentText, content_type=ContentType.objects.get_for_model(Episode))
            new_comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect(redirect_url, **redirect_kwargs)
        
        # If Not Valid
        else:
            error_messages = comment_form.errors.as_text()
            messages.success(request, error_messages)
            return redirect(redirect_url, **redirect_kwargs)
        

def delete_comment(request, content_type, id, comment_id, resolution, season=None, episode=None):
    """ Delete Comment """
    if request.method == 'POST':
        redirect_url, redirect_kwargs = redirect_data(id=id, content_type=content_type, resolution=resolution, season=season, episode=episode)
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect(redirect_url, **redirect_kwargs)


def edit_comment(request, content_type, id, resolution, season=None, episode=None):
    """ Edit Comment """
    redirect_url, redirect_kwargs = redirect_data(id=id, content_type=content_type, resolution=resolution, season=season, episode=episode)
    if request.method == 'POST':
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():
            editText = edit_form.cleaned_data.get('commentText')
            comment_id = edit_form.cleaned_data.get('commentId')
            comment = Comment.objects.get(id=comment_id)
            comment.commentText = editText
            comment.save()
        return redirect(redirect_url, **redirect_kwargs)