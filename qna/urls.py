from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('qna/', qna, name="qna"),
    path('writet/', writet, name="writet"),
    path('postsearches/', postsearches, name="postsearches"),
]