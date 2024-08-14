from django.urls import path
from .views import news_analysis_view

app_name = 'news'

urlpatterns = [
    path('news/', news_analysis_view, name='news'),
]
