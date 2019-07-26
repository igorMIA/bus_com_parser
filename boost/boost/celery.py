import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boost.settings')


app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'scrapy_bus_station_1_hour': {
        'task': 'scrapy_bus_station',
        'schedule': crontab(minute='*/90'),
        'args': [],
    },
    'check_parser_status_5_min': {
        'task': 'check_parser_status',
        'schedule': crontab(minute='*/5'),
        'args': [],
    },
}

app.conf.timezone = 'UTC'

if __name__ == '__main__':
    app.start()
