# techtask
techtask: low price calendar

# Python 3.8.10

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
bash install_redis.sh

# run app
python -m flask run

# run celery
venv/bin/celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid

# run worker
venv/bin/celery worker -A app.celery --loglevel=INFO
