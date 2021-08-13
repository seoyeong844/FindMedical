from django.db import models
from django.forms.fields import BooleanField
from django.conf import settings
from user.models import Users

# Create your models here.
class Qna(models.Model):
    writer = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="작성자")
    title = models.CharField(max_length=200, verbose_name="제목")
    body = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')
    pub_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="작성일")
    update = models.DateTimeField(auto_now=True, null=True, verbose_name="최종수정일")

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'board3'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'