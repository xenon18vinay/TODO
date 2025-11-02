from django.urls import path
from . import views
urlpatterns = [
    path("",views.todo_list, name="todo_list"),
    path('toggle/<int:pk>',views.toggle_todo,name='toggle_todo'),
]