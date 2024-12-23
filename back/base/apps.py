from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        post_migrate.connect(self.setup_periodic_tasks, sender=self)

    def setup_periodic_tasks(self, **kwargs):
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        import json

        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*',
        )
        task, created = PeriodicTask.objects.get_or_create(
            name='Check assignment deadlines',
            defaults={
                'crontab': schedule,
                'task': 'base.tasks.check_deadlines',
                'args': json.dumps([]),
            }
        )
        if not created:
            task.crontab = schedule
            task.save()