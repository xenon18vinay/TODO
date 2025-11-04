from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from datetime import timedelta
from .forms import ToDoForm, SignUpForm
from .models import ToDoModel
from django.views.generic import CreateView

# views.py (inside todo_list)
from datetime import timedelta
import re

def _parse_todo_time_to_seconds(value):
    """
    Accepts:
      - integer seconds as string or int -> returns int seconds
      - "HH:MM:SS" or "MM:SS" -> returns seconds
      - "0:00:00" -> returns 0
      - None/invalid -> returns 0
    """
    if value is None:
        return 0

    # If it's already a timedelta
    if isinstance(value, timedelta):
        return int(value.total_seconds())

    s = str(value).strip()

    # Empty
    if s == "" or s in {"0", "0:00", "0:00:00"}:
        return 0

    # If purely numeric (seconds)
    if re.fullmatch(r"-?\d+", s):
        try:
            return max(0, int(s))
        except ValueError:
            return 0

    # Pattern HH:MM:SS or MM:SS
    if ":" in s:
        parts = s.split(":")
        try:
            parts = [int(p) for p in parts]
        except ValueError:
            return 0

        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            hours = 0
            minutes, seconds = parts
        else:
            # unexpected number of fields, bail safely
            return 0

        if hours < 0 or minutes < 0 or seconds < 0:
            return 0

        return hours * 3600 + minutes * 60 + seconds

    # Fall back
    try:
        return int(float(s))
    except Exception:
        return 0

@login_required
def todo_list(request):
    form = ToDoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)

            # Robustly parse various todo_time formats:
            todo_time_value = request.POST.get('todo_time') or request.POST.get('todo_time_hidden') or request.POST.get('todo_time_field') or form.cleaned_data.get('todo_time')
            seconds = _parse_todo_time_to_seconds(todo_time_value)

            temp.todo_time = timedelta(seconds=seconds)
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
