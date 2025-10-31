from django.shortcuts import render, redirect
from .forms import ToDoForm
# Create your views here.
def todo_list(request):
    if request.method == "POST":
        form =  ToDoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('todo_list')
    else:
        to_do_form = ToDoForm()
    return render(request,'list/list.html', context={'form':to_do_form})