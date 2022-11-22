#!/bin/bash

/wait

cd /project

celery -A demo beat -l debug -S redbeat.RedBeatScheduler