#!/bin/bash

python manage.py migrate
yes | python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
