from django.urls import path
from . import views

app_name = 'tts_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('status/', views.check_status, name='check_status'),
]