from django.contrib import admin
from .models import Qna
from .forms import PostForm
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Qna)
class QnaAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    list_display = ('title', 'writer', 'hits', 'pub_date', 'update')
    readonly_fields = ['pub_date']
    list_display_links = list_display
    

#admin.site.register(Qna, QnaAdmin)