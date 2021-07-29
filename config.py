from os import environ


REDIS_HOST = '0.0.0.0'
REDIS_PORT = 6379
BROKER_URL = environ.get('REDIS_URL', 'redis://{host}:{port}/0'.format(
    host=REDIS_HOST, port=str(REDIS_PORT)))
CELERY_RESULT_BACKEND = BROKER_URL

DB_URL = 'mongodb://localhost:27017/calendar'

KIWI_PARTNER = 'shertest'
KIWI_FLIGHTS_URL = 'https://api.skypicker.com/flights'
KIWI_FLIGHT_CHECK = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
