from movie_app.models import Movie
from series_app.models import Series
from movieStreamingApp.models import WatchHistory

from datetime import timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

@login_required
def add_watchHistory(request, id, content_type):
    try:
        
        watchHistory_object, created = WatchHistory.objects.get_or_create(user=request.user, content_type=content_type, object_id=id)
        watchHistory_object.addedDateTime = timezone.now() if not created else watchHistory_object.addedDateTime
        watchHistory_object.save()

        # delete watch history before 368 days ago
        limit_time = timezone.now() - timedelta(days=368)
        WatchHistory.objects.filter(user=request.user, addedDateTime__lt=limit_time).delete()

        # delete if saved items for a user is more than 500
        limit_count = 500
        history_count = WatchHistory.objects.filter(user=request.user).count()
        if history_count > limit_count:
            delete_count = history_count - limit_count
            to_delete = WatchHistory.objects.filter(user=request.user).order_by('addedDateTime')[:delete_count]
            
            for item in to_delete:
                item.delete()

    except Exception as e:
        raise e