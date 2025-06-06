import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.beat_schedule = {
    "run-overdue-loan-reminder": {
        "task": "task.check_overdue_loans",
        "schedule": crontab(minute='*'),  # runs every minute
    },
}
