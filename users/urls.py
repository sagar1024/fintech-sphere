from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'users'  # Defining the namespace

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('invest/', views.invest_view, name='invest'),
]
