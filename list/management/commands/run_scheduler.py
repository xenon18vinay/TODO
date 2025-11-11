from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore,register_job
from list.task import create_daily_elements_task


class Command(BaseCommand):
    help = 'Runs APScheduler as a blocking process to manage scheduled tasks.'

    def handle(self, *args, **options):
        scheduler =  BlockingScheduler(timezone=settings.TIME_ZONE)

        try:
           scheduler.add_jobstore(DjangoJobStore(), 'default')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to add job store:{e}"))
            return

        scheduler.add_job(
            func=create_daily_elements_task,
            trigger='cron',
            hour=12,
            minute=4,
            id='create_daily_elements',
            replace_existing = True,
            misfire_grace_time=900,
        )
        self.stdout.write(self.style.SUCCESS("Starting APScheduler process... Press Ctrl+C to exit."))

        try:
            scheduler.start()
            print(scheduler.get_jobs())
        except(KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.NOTICE("Scheduler process stopped gracefully."))
            scheduler.shutdown()