from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('comhospital/', comhospital, name="comhospital"),
    path('writes/', writes, name="writes"),
    path('postsearch/', postsearch, name="postsearch"),
]