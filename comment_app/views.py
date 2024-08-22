from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from .models import Comment
from movie_app.models import Movie
from .forms import CommentForm, EditForm
from series_app.models import Series, Episode, Season


@login_required
def create_comment(request, content_type, id, season=None, episode=None):
    """ Add New Comments To The Comment Table """
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        # If Valid
        if comment_form.is_valid():
            try:
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
                return HttpResponse(status = 200)
            
            except Exception as e:
                raise e

        # If Invalid
        else:
            messages.error(request, comment_form.errors.as_text())

        return HttpResponse(status = 500)
        

@login_required
def delete_comment(request, comment_id):
    """ Delete Comment """
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            messages.success(request, 'Comment deleted successfully')
            return HttpResponse(status = 200)
        except Exception as e:
            raise e
            return HttpResponse(status = 500)
    

@login_required
def edit_comment(request):
    """ Edit Comment """
    if request.method == 'POST':
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():

            try:
                editText = edit_form.cleaned_data.get('commentText')
                comment_id = edit_form.cleaned_data.get('commentId')
                comment = Comment.objects.get(id=comment_id)
                comment.commentText = editText
                comment.save()
                messages.success(request, 'Comment edited successfully')
                return HttpResponse(status = 200)
            
            except Exception as e:
                raise e

        else:
            messages.error(request, edit_form.errors.as_text())

        return HttpResponse(status = 500)
    

def load_comment(request, content_type, id, episode=None, season=None):
    """ Get Comments """
    if content_type == 'movies':
        model = Movie
    elif content_type == 'series':
        model = Episode
        target_series = Series.objects.get(id=id)
        target_season = target_series.season_set.get(season=season) 
        target_episode = target_season.episode_set.get(episode=episode)
        id = target_episode.id
    
    # Get list of (id, commentText) tuples
    fetch_comments = list(Comment.objects.filter(object_id=id, content_type=ContentType.objects.get_for_model(model)).values_list('user__id','user__username','id','commentText','addedDateTime').order_by('-addedDateTime'))
    comments = []

    # Turn it into list of dictionaries
    for x in fetch_comments:
        comments.append({
            'userId': x[0],
            'userName': x[1],
            'commentId': x[2],
            'commentText': x[3], 
            'addedDateTime': x[4].isoformat()
        })

    # Paginator slices []
    paginator = Paginator(comments, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Send the sliced [] as JSON
    return JsonResponse({'comments': page_obj.object_list, 'hasNext': page_obj.has_next()})
    

#########################################################################
    

""" Old Codes Without JS Fetch """

'''
def delete_comment(request, content_type, id, comment_id, resolution, season=None, episode=None):
    """ Delete Comment """
    if request.method == 'POST':
        redirect_url, redirect_kwargs = redirect_data(id=id, content_type=content_type, resolution=resolution, season=season, episode=episode)
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect(redirect_url, **redirect_kwargs)
'''

'''
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
'''

'''
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
'''

'''
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
'''