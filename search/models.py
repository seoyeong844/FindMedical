from django.db import models
from django.forms.fields import BooleanField

#증상검색 checkbox
class Symptom:
    published = BooleanField()