from celery.schedules import crontab


CELERY_IMPORTS = ('app.taskapp.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    # TIME_ZONE = UTC
    # Almaty time = UTC + 6
    # Executes every day at 12 a.m. by Almaty time
    'add-every-night-crontab': {
        'task': 'app.taskapp.tasks.update_flights',
        'schedule': crontab(hour=(0 - 6 + 24) % 24, minute=0),
        'args': (16, 16),
    }
}
