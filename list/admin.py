from django.contrib import admin
from .models import ToDoModel
# Register your models here.

class ToDoModelAdmin(admin.ModelAdmin):
    list_display = ['id','to_do','to_user','checker','is_hidden']
    list_filter = ['checker','is_hidden']
    search_fields = ['to_user__username']
    list_per_page = 30

admin.site.register(ToDoModel,ToDoModelAdmin)

