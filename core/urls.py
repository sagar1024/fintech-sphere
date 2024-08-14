"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#Importing the req libs
from django.contrib import admin
from django.urls import path, include
from app import views as app_views
from users import views as user_views
from news import views as news_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.index, name='home'),
    path('search/', app_views.search, name='search'),
    path('predict/<str:ticker_value>/<str:number_of_days>/', app_views.predict, name='predict'),
    path('ticker/', app_views.ticker, name='ticker'),

    #Include the users app URLs with namespace
    path('users/', include('users.urls', namespace='users')),
    path('profile/', user_views.profile_view, name='profile'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    
    #Include the news app URLs
    path('news/', news_views.news_analysis_view, name='news'),
]
