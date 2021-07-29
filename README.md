# techtask
techtask: low price calendar

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

bash install_redis.sh

python -m flask run

venv/bin/celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid
venv/bin/celery worker -A app.celery --loglevel=INFO
