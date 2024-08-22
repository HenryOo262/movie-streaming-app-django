from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def auth_profile(request):
    if request.method == 'GET':
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        profile_form = ProfileForm(initial=initial_data)
        return render(request, 'profile.html', {'form': profile_form})
    elif request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            try:
                username = profile_form.cleaned_data['username']
                email = profile_form.cleaned_data['email']
                first_name = profile_form.cleaned_data['first_name']
                last_name = profile_form.cleaned_data['last_name']
                user = User.objects.filter(id=request.user.id)
                user.update(username=username, email=email, first_name=first_name, last_name=last_name)
                messages.success(request, 'Profile updated successfully')
                return redirect('auth_app.auth_profile')
            except Exception as e:
                print(e)
                messages.error(request, 'Error updating profile')
        return render(request, 'profile.html', {'form': profile_form})


@login_required
def auth_passwordChange(request):
    if request.method == 'GET':
        passwordChange_form = PasswordChangeForm(request.user)
        return render(request, 'passwordChange_form.html', {'form': passwordChange_form})
    elif request.method == 'POST':
        passwordChange_form = PasswordChangeForm(user=request.user, data=request.POST)
        if passwordChange_form.is_valid():
            try:
                passwordChange_form.save()
                logout(request)
                messages.info(request, 'Password changed successfully. Please login again.')
                return redirect('auth_app.auth_login')
            except Exception as e:
                print(e)
                messages.error(request, 'Error changing password')
        return render(request, 'passwordChange_form.html', {'form': passwordChange_form})


def auth_register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'register_form.html', {'form': register_form})
    elif request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                register_form.save()
                messages.success(request, 'Registered successfully')
                return redirect('auth_app.auth_login')
            except Exception:
                print(Exception)
                messages.error(request, 'Error registering user')
        return render(request, 'register_form.html', {'form': register_form})


def auth_login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'login_form.html', {'form': login_form})
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user) 
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, 'login_form.html', {'form': login_form})


def auth_logout(request):
    logout(request)
    return redirect('home')