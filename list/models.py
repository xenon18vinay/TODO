from django.db import models
from django.template.context_processors import request
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
# Create your models here.

class RecurringTodoTemplate(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    task_name=models.TextField(max_length=500)
    todo_time=models.DurationField(default=timedelta(seconds=0))
    is_active=models.BooleanField(default=True)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_visible=models.DateTimeField(default=True)
    class Meta:
        indexes = [
            models.Index(fields=['user','is_active'])
        ]
    def __str__(self):
        return f"{self.user.username} - {self.task_name}"
class ToDoModel(models.Model):
    to_do = models.CharField(max_length=500)
    to_user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    checker = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    timer=models.DurationField(default=timedelta(0))
    todo_time=models.DurationField(default=timedelta(0))
    template = models.ForeignKey(RecurringTodoTemplate,on_delete=models.SET_NULL,null=True,blank=True,related_name='instances')


    class Meta:
        indexes = [
            models.Index(fields=['to_user','is_hidden','-created_at']),
            models.Index(fields=['template'])
        ]



    def __str__(self):
        return f"{self.to_user.username}"
