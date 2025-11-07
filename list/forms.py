from django.contrib.auth.forms import UserCreationForm
from .models import ToDoModel
from django import forms

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoModel
        fields = ['to_do', 'todo_time','is_everyday']
        todo_time = forms.IntegerField(
            widget=forms.HiddenInput(attrs={'id': 'todoTimeHidden'}),
            required=False,
            initial=0
        )
        widgets = {
            'to_do': forms.TextInput(attrs={
                'placeholder': 'Add a task...',
                'class': 'task-input-field',
                'autocomplete': 'off'
            }),
            'todo_time': forms.HiddenInput(attrs={
                'id': 'todoTimeHidden',
                'value': '0'
            }),
            'is_everyday': forms.CheckboxInput(attrs={
                'style': 'display: none;'
            })
        }
        labels = {
            'to_do': '',
            'todo_time': '',
            'is_everyday': ''
        }


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username',)
