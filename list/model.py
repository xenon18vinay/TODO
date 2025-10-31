from django.db import models


class ToDoModel(models.Model):
    to_do = models.CharField(max_length=500)
