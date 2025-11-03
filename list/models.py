from django.db import models
from django.template.context_processors import request
from django.contrib.auth.models import User

# Create your models here.
class ToDoModel(models.Model):
    to_do = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    to_user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    checker = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)