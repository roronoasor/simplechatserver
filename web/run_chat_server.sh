#!/bin/sh
python manage.py collectstatic --noinput
daphne solchatserver.asgi:application -b 0.0.0.0 -p 8000