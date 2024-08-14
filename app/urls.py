from django.contrib import admin
from django.urls import path, include
from . import views
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name="index"),
    path('search/', search),
    path('predict/<str:ticker_value>/<str:number_of_days>/', predict),
    path('ticker/', ticker),
]