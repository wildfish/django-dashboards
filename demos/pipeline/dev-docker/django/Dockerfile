FROM python:3.9-slim

RUN mkdir /build
WORKDIR /build

# Build process dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# TODO temp until pipelines ready
COPY ./django-wildcoeus-pipelines/ /build/django-wildcoeus-pipelines/
RUN pip install ./django-wildcoeus-pipelines

# Full python requirements to support development
COPY ./demo_pipelines/requirements.txt /build/requirements.txt
RUN pip install -r requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# Run Django
WORKDIR /project
CMD ["/project/dev-docker/django/run.sh"]