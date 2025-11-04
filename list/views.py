from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from datetime import timedelta
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
        all_to_do = ToDoModel.objects.all().filter(to_user=request.user,is_hidden=False).order_by('-created_at')
        to_do_form = ToDoForm()
    return render(request,'list/list.html', context={'form':to_do_form,'todo_list':all_to_do})
@login_required
@require_POST
def toggle_todo(request,pk):
    todo = get_object_or_404(ToDoModel,id=pk,to_user=request.user)
    todo.checker = not todo.checker
    todo.save()
    return redirect('todo_list')

def timer(request,pk):
    todo = get_object_or_404(ToDoModel,id=pk,to_user=request.user)
    seconds_str = request.POST.get('duration_in_seconds')
    new_duration=timedelta(seconds=int(seconds_str))
    todo.timer = todo.timer+ new_duration
    todo.save()
    return redirect('todo_list')

def delete_todo(request,pk):
    todo=get_object_or_404(ToDoModel,id=pk,to_user=request.user)
    todo.is_hidden = True
    todo.save()
    return redirect('todo_list')
class SignUpView(CreateView):
     form_class = SignUpForm
     template_name = 'registration/signup.html'
     success_url = reverse_lazy('login')