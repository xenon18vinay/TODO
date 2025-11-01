from django.shortcuts import render, redirect
from .forms import ToDoForm
from .models import ToDoModel
# Create your views here.
def todo_list(request):
    if request.method == "POST":
        form =  ToDoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('todo_list')
    else:
        all_to_do = ToDoModel.objects.all().order_by('-created_at')
        to_do_form = ToDoForm()
    return render(request,'list/list.html', context={'form':to_do_form,'todo_list':all_to_do})