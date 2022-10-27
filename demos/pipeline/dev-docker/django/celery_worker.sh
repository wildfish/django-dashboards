#!/bin/bash

/wait

cd /project

celery -A demo worker -l info