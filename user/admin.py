from django.contrib import admin
from .models import Users
# Register your models here.

@admin.register(Users)

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'user_pw',
        'user_name',
        'user_email',
    )