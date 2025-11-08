from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from datetime import timedelta
from .forms import ToDoForm, SignUpForm
from .models import ToDoModel,UserProfile
from django.views.generic import CreateView


# views.py (inside todo_list)
from datetime import timedelta
import re


@login_required
def todo_list(request):
    form = ToDoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            try:
                todo_time_value = int(request.POST.get('todo_time', 0))
            except (ValueError, TypeError):
                todo_time_value = 0
            if temp.is_everyday:
                profiler = get_object_or_404(UserProfile,user=request.user)

                every_day_list = profiler.every_day.copy()
                tupler = (temp.to_do, todo_time_value)
                every_day_list.append(tupler)
                profiler.every_day = every_day_list
                profiler.save()
            temp.todo_time = timedelta(seconds=todo_time_value)
            temp.to_user = request.user
            temp.save()
        return redirect('todo_list')
    all_to_do = ToDoModel.objects.filter(to_user=request.user, is_hidden=False).order_by('-created_at')
    to_do_form = ToDoForm()
    return render(request, 'list/list.html', context={
        'form': to_do_form,
        'todo_list': all_to_do
    })


@login_required
@require_POST
def toggle_todo(request, pk):
    todo = get_object_or_404(ToDoModel, id=pk, to_user=request.user)
    _perform_toggle(todo)
    return redirect('todo_list')


@login_required
@require_POST
def time_spend(request, pk):
    todo = get_object_or_404(ToDoModel, id=pk, to_user=request.user)
    seconds_str = request.POST.get('duration_in_seconds')

    if seconds_str:
        # Add elapsed time to stopwatch
        new_duration = timedelta(seconds=int(seconds_str))
        todo.timer = todo.timer + new_duration
        todo.save()

        if todo.timer >= todo.todo_time>timedelta(seconds=0) and not todo.checker :
            _perform_toggle(todo)

    return redirect('todo_list')


def _perform_toggle(todo):
    todo.checker = not todo.checker
    todo.save()


@login_required
@require_POST
def delete_todo(request, pk):
    todo = get_object_or_404(ToDoModel, id=pk, to_user=request.user)
    todo.is_hidden = True
    todo.save()
    return redirect('todo_list')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
