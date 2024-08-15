from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_login, name='auth_app.auth_login'),
    path('logout/', views.auth_logout, name='auth_app.auth_logout'),
    path('register/', views.auth_register, name='auth_app.auth_register'),
    path('profile/', views.auth_profile, name='auth_app.auth_profile'),
    path('passwordChange/', views.auth_passwordChange, name='auth_app.auth_passwordChange'),
]
