from functools import wraps
from django.shortcuts import render


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, '403.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


'''
from django.contrib.auth.decorators import user_passes_test

def check_superuser(user):
    return user.is_superuser

@user_passes_test(check_superuser)
def view_func(request):
    pass
'''