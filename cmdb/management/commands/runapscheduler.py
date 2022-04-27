from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger

from Fupan.views import auto_update
from Utils.mode import get_today_time


def my_job():
    # Your job processing logic here...
    now = get_today_time("%Y-%m-%d")
    datetime = now.rjust(10,'0')
    auto_update(datetime)
    print("my_job.")
    pass


# The `close_old_connections` decorator ensures that database connections, that have become unusable or are obsolete,
# are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database. It helps to prevent the
    database from filling up with old historical records that are no longer useful.

    :param max_age: The maximum length of time to retain historical job execution records. Defaults
                    to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            #trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            trigger=CronTrigger(
                day_of_week="mon-sun", hour="16", minute="00"
            ),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        print("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        print(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            print("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            scheduler.shutdown()
            print("Scheduler shut down successfully!")
