import json
from datetime import datetime

import requests
import celery

from app import db
import config


@celery.task()
def update_flights(*args):
    partner = config.KIWI_PARTNER
    adults = 1

    today = datetime.utcnow().date()
    next_mon = '01' if today.month == 12 else today.month + 1
    next_year = today.year + 1 if today.month == 12 else today.year
    date_from = f'{today.day}%2F{today.month}%2F{today.year}'
    date_to = f'{today.day}%2F{next_mon}%2F{next_year}'

    fly_direction = [
        ('ALA', 'TSE'),
        ('TSE', 'ALA'),
        ('ALA', 'MOW'),
        ('MOW', 'ALA'),
        ('ALA', 'CIT'),
        ('CIT', 'ALA'),
        ('TSE', 'MOW'),
        ('MOW', 'TSE'),
        ('TSE', 'LED'),
        ('LED', 'TSE'),
    ]

    payloads = []

    for fly_from, fly_to in fly_direction:
        url = f'''{config.KIWI_FLIGHTS_URL}?fly_from={fly_from}&fly_to={fly_to}&
            date_from={date_from}&date_to={date_to}&adults={adults}&partner={partner}'''

        response = requests.get(url)

        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            return False

        flights = json.loads(response.content)

        for flight in flights['data']:
            payload_to_insert = {}
            payload_to_insert['id'] = flight['id']
            payload_to_insert['cityCodeFrom'] = flight['cityCodeFrom']
            payload_to_insert['cityCodeTo'] = flight['cityCodeTo']
            payload_to_insert['dTime'] = datetime.fromtimestamp(flight['dTime']).strftime('%d-%m-%Y %H:%M:%S')
            payload_to_insert['aTime'] = datetime.fromtimestamp(flight['aTime']).strftime('%d-%m-%Y %H:%M:%S')
            payload_to_insert['price'] = flight['price']
            payload_to_insert['booking_token'] = flight['booking_token']
            payload_to_insert['currency'] = flights['currency']

            payloads.append(payload_to_insert)

    try:
        db.calendar.delete_many({})
        db.calendar.insert_many(payloads)
    except Exception as e:
        print(e)
        return False

    return True
