from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ToDoModel
from django import forms

class ToDoForm(forms.ModelForm):
    todo_time = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'todoTimeHidden'}),
        required=False,
        initial=0
    )
    class Meta:
        model = ToDoModel
        fields = ['to_do', 'todo_time','is_everyday']

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
            'is_everyday': forms.HiddenInput()

        }
        labels = {
            'to_do': '',
            'todo_time': '',
            'is_everyday': ''
        }

class EmailOrUsernameLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username','email')
