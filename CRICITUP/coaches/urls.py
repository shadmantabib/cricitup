from django.contrib import admin
from django.urls import path, include
from . import views

app_name='coaches'
urlpatterns = [
    # path('', views.home, name='home'),
    # path('teams/', views.teams, name='teams'),
    # path('players/',views.players,name='players'),
    path('', views.coaches_list, name='coaches'),
]