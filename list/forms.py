from .model import ToDoModel
from django import forms

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoModel
        fields = ['to_do']

