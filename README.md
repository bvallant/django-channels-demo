# django-channels-demo

## Setup
1. Install and run Redis in default config
1. `[master][~/projects/django-channels-demo/src]$ pip install -r requirements.txt`

## Run

In one terminal

    [master][~/projects/django-channels-demo/src/channels-demo]$ python manage.py runserver


and in the other

    [master][~/projects/django-channels-demo/src/channels-demo]$ celery -A demo worker --loglevel=info
