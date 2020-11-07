from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('baseline', views.baseline_products),
    path('driver', views.driver_products),
    path('elite', views.elite_products),
    path('coming-soon', views.coming_soon),
    path('logout', views.logout),
]