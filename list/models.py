from django.db import models
from django.template.context_processors import request
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
# Create your models here.
class ToDoModel(models.Model):
    to_do = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    to_user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    checker = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    timer=models.DurationField(default=timedelta(0))
    is_everyday=models.BooleanField(default=False)
    todo_time=models.DurationField(default=timedelta(0))

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    every_day = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.username}"
