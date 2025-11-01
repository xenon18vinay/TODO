from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import ToDoForm,SignUpForm
from .models import ToDoModel
from django.views.generic import CreateView
# Create your views here.
@login_required
def todo_list(request):
    if request.method == "POST":
        form =  ToDoForm(request.POST)
        if form.is_valid():
            temp=form.save(commit=False)
            temp.to_user = request.user
            form.save()
        return redirect('todo_list')
    else:
        all_to_do = ToDoModel.objects.all().filter(to_user=request.user).order_by('-created_at')
        to_do_form = ToDoForm()
    return render(request,'list/list.html', context={'form':to_do_form,'todo_list':all_to_do})

class SignUpView(CreateView):
     form_class = SignUpForm
     template_name = 'registration/signup.html'
     success_url = reverse_lazy('login')