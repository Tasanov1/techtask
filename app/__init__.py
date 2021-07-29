import json
from bson import json_util

from flask import Flask, request
from flask_pymongo import PyMongo
from celery import Celery
import requests

import celeryconfig

app = Flask(__name__)
app.config.from_object('config')
mongodb_client = PyMongo(app, uri=app.config['DB_URL'])
db = mongodb_client.db


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)


@app.route('/flights')
def get_flights():
    if request.args.get('fly_from') is None or request.args.get('fly_to') is None:
        return {'detail': '"fly_from" and "fly_to" - required params'}, 400
    cursor = db.calendar.find({'cityCodeFrom': request.args.get('fly_from'),
                               'cityCodeTo': request.args.get('fly_to')}).sort('price').limit(5)
    flights = json.loads(json_util.dumps(cursor))

    return {'flights': flights}, 200


@app.route('/check_flights')
def check_flight():
    if request.args.get('booking_token') is None:
        return {'detail': '"booking_token" - required param'}, 400

    url = f'{app.config["KIWI_FLIGHT_CHECK"]}?bnum=1&pnum=1&booking_token={request.args.get("booking_token")}'
    response = requests.get(url)

    if response.status_code != 200:
        return {}, 500

    data = json.loads(response.content)

    return {'flights_invalid': data['flights_invalid'],
            'price_change': data['price_change'],
            'flights_price': data['flights_price'],
            'currency': data['currency']}, 200


if __name__ == '__main__':
    app.run()
