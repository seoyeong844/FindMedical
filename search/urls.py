from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('search/', search, name="search"),
    path('cervical/', cervical, name="cervical"),
    path('vater/', vater, name="vater"),
    path('stomach/', stomach, name="stomach"),
    path('thyroid/', thyroid, name="thyroid"),
    path('lung/', lung, name="lung"),
    path('breast/', breast, name="breast"),
    path('liver/', liver, name="liver"),
    path('both/', both, name="both"),
]