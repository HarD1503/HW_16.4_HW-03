import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'action_every_monday_8am':
        {
        'task': 'news.tasks.notify_weekly_posts_task',
        #'schedule': crontab(minute='*/5'),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': ()
        }
    }
#app.conf.update(
#    timezone='Europe/Moscow',
#    enable_utc=True, # Храним время в UTC
#    worker_hijack_root_logger=False, # Переопределяем настройки логгирования
#)
app.conf.timezone = 'UTC'