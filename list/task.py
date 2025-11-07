from datetime import timedelta

from list.models import UserProfile, ToDoModel
from django_apscheduler.jobstores import DjangoJobStore,register_job


def create_daily_elements_task():
    for user_profile in UserProfile.objects.all():
        user = user_profile.user
        every_day_list = user_profile.every_day
        if not every_day_list:
            continue
        print(f"Processing everyday tasks for user: {user.username}")
        for tup in every_day_list:
            try:
                ToDoModel.objects.create(
                    to_user= user,
                    to_do= tup[0],
                    todo_time=timedelta(seconds=tup[1]),
                    is_everyday=True
                )
            except Exception as e:
                print(f"  Error creating task for {user.username}: {e}")

    print("Finished creating all daily elements.")
