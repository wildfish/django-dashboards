FROM python:3.11.0-slim

RUN mkdir /build
WORKDIR /build

# Build process dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libc6-dev \
    python3-dev \
    python-tk \
    git \
    && rm -rf /var/lib/apt/lists/*

# Build pyodbc dependencies
RUN apt-get update \
    && apt-get install -y g++ \
    && apt-get install -y unixodbc-dev

# Python requirements
COPY ./requirements.txt /build/requirements.txt
RUN pip install -r requirements.txt

# todo: temp until we can get django-wildcoeus installable from git
COPY django-wildcoeus-0.0.1.tar.gz  .
RUN pip install django-wildcoeus-0.0.1.tar.gz

ENV WAIT_VERSION 2.9.0
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# Run Django
WORKDIR /project
CMD /wait && "/project/dev-docker/django/run.sh"
