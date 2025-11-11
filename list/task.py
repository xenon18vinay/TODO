from list.models import RecurringTodoTemplate, ToDoModel


def create_daily_elements_task():
    for template in RecurringTodoTemplate.objects.filter(is_active=True):
        ToDoModel.objects.create(
            to_do=template.task_name,
            to_user_id=template.user_id,
            todo_time=template.todo_time
        )
    print("Finished creating all daily elements.")
