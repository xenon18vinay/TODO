from django.contrib.auth.forms import UserCreationForm

from .models import ToDoModel
from django import forms

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoModel
        fields = ['to_do']

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username',)
