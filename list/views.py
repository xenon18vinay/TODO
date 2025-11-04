from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from datetime import timedelta
from .forms import ToDoForm, SignUpForm
from .models import ToDoModel
from django.views.generic import CreateView


@login_required
def todo_list(request):
    form = ToDoForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)

            # Fix: Handle the todo_time properly
            todo_time_value = request.POST.get('todo_time', '0')

            # Convert to integer, handling various formats
            try:
                if ':' in str(todo_time_value):
                    # If it's in time format like '00:00:00', set to 0
                    todo_time_seconds = 0
                else:
                    # Otherwise convert to int
                    todo_time_seconds = int(todo_time_value)
            except (ValueError, AttributeError):
                todo_time_seconds = 0

            temp.todo_time = timedelta(seconds=todo_time_seconds)
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

        # Auto-complete if stopwatch exceeds estimated time
        if todo.timer >= todo.todo_time and not todo.checker:
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
