"""fmproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from fmapp.views import home
import fmapp.views
import comhospital.views
import qna.views
import search.views
import user.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', home, name="home"),
    path('fmapp/', include('fmapp.urls')),
    path('user/', include('user.urls')),
    path('fmapp/writef/<int:community_id>', fmapp.views.writef, name="writef"),
    path('fmapp/new', fmapp.views.new, name='new'),
    path('fmapp/postcreate', fmapp.views.postcreate, name='postcreate'),
    path('fmapp/edit', fmapp.views.edit, name='edit'),
    path('fmapp/postupdate/<int:community_id>', fmapp.views.postupdate, name='postupdate'),
    path('fmapp/postdelete/<int:community_id>', fmapp.views.postdelete, name='postdelete'),
    path('comhospital/', include('comhospital.urls')),
    path('comhospital/writes/<int:comhospital_id>', comhospital.views.writes, name="writes"),
    path('comhospital/news', comhospital.views.news, name='news'),
    path('comhospital/postcreates', comhospital.views.postcreates, name='postcreates'),
    path('comhospital/edits', comhospital.views.edits, name="edits"),
    path('comhospital/postupdates/<int:comhospital_id>', comhospital.views.postupdates, name='postupdates'),
    path('comhospital/postdeletes/<int:comhospital_id>', comhospital.views.postdeletes, name='postdeletes'),
    path('qna/', include('qna.urls')),
    path('qna/writet/<int:qna_id>', qna.views.writet, name="writet"),
    path('qna/newt', qna.views.newt, name='newt'),
    path('qna/postcreatet', qna.views.postcreatet, name='postcreatet'),
    path('qna/editt', qna.views.editt, name='editt'),
    path('qna/postupdatet/<int:qna_id>', qna.views.postupdatet, name='postupdatet'),
    path('qna/postdeletet/<int:qna_id>', qna.views.postdeletet, name='postdeletet'),
    path('search/', include('search.urls')),
    path('search/result', search.views.result, name="result"),
] #+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #커뮤니티에서 사진 받는 경우 해당 static추가...?!
#static을 병렬적으로 더해주는 형태

#summernote
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns += [path('summernote/', include('django_summernote.urls'))]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)