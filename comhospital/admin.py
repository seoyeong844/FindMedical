from django.contrib import admin
from .models import ComHospital
from .forms import PostForm
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(ComHospital)
class ComHospitalAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    list_display = ('title','writer', 'hits', 'pub_date', 'update')
    readonly_fields = ['pub_date']
    list_display_links = list_display

#admin.site.register(ComHospital, ComHospitalAdmin)