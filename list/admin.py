from django.contrib import admin
from .models import ToDoModel,UserProfile
# Register your models here.

class ToDoModelAdmin(admin.ModelAdmin):
    list_display = ['id','to_do','to_user','checker','is_hidden','is_everyday']
    list_filter = ['checker','is_hidden']
    search_fields = ['to_user__username']
    list_per_page = 30

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','every_day','user__email']
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(ToDoModel,ToDoModelAdmin)