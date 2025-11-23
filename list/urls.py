from django.urls import path
from . import views
urlpatterns = [
    path("",views.todo_list, name="todo_list"),
    path('toggle/<int:pk>',views.toggle_todo,name='toggle_todo'),

    path('delete/<int:pk>', views.delete_todo, name='delete_todo'),
    path('delete_recurring/<int:pk>',views.delete_recurring, name='delete_recurring'),
    path('timer/<int:pk>', views.time_spend,name='time_spend'),
    path('update_recurring/<int:pk>', views.update_recurring, name='update_recurring'),
]