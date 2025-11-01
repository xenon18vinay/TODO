from django.db import models

# Create your models here.
class ToDoModel(models.Model):
    to_do = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
