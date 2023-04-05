#!/bin/bash
cd /project

./manage.py migrate
./manage.py sample_vehicle_data
./manage.py runserver 0:8000
