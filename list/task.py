from list.models import UserProfile, ToDoModel
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def create_daily_elements_task():
    logger.info("=" * 50)
    logger.info("Starting daily task creation job...")
    logger.info("=" * 50)
    
    user_profiles = UserProfile.objects.all()
    logger.info(f"Found {user_profiles.count()} user profiles")
    
    total_created = 0
    
    for user_profile in user_profiles:
        user = user_profile.user
        every_day_list = user_profile.every_day
        
        if not every_day_list:
            logger.info(f"No everyday tasks for user: {user.username}")
            continue
            
        logger.info(f"Processing {len(every_day_list)} everyday tasks for user: {user.username}")
        
        for task_data in every_day_list:
            try:
                todo_obj = ToDoModel.objects.create(
                    to_user=user,
                    to_do=task_data[0],
                    todo_time=timedelta(seconds=task_data[1]),
                    is_everyday=True
                )
                total_created += 1
                logger.info(f"  ✓ Created task: '{task_data[0]}' for {user.username}")
            except Exception as e:
                logger.error(f"  ✗ Error creating task for {user.username}: {e}")
                logger.error(f"    Task data: {task_data}")
    
    logger.info("=" * 50)
    logger.info(f"Finished! Created {total_created} daily tasks")
    logger.info("=" * 50)
