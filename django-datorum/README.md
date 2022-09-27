This would be the datorum lib/open source project we use for all clients.

### Server sent events (experimental for HTMX version only atm)

No direct support has been added for now, however our demo includes an SSE component example.  

The dashboard example of this can b seen at http://127.0.0.1:8000/dashboards/SSEDashboard/ when running the demo.

In order for the demo to run, you will also need to start pushpin. This allows the sending of events via background tasks, aids with 
event distribution

* Create a config file to tell pushpin where to route events.
   
        echo '* localhost:8000' > config
   
* Start a docker instance with:  
    
        docker run \
          -d \
          -p 7999:7999 \
          -p 5560-5563:5560-5563 \
          -v routes:/etc/pushpin/routes \
          --rm \
          --name pushpin \
          fanout/pushpin

* Start a management command to push some data (this could be a async task/celery etc also)

        python manage.py send_sse



#### Using SSE in your project

This is experimental and the aim is to move this into the main library, however for now, the additional steps/config
required to get this working are detailed below:

* Install `django_eventstream` (without channels) https://github.com/fanout/django-eventstream, adding 

		INSTALLED_APPS = [
		    ...
		    'django_eventstream',
		]

		MIDDLEWARE = [
		    'django_grip.GripMiddleware',
   		     ...
		]

        GRIP_URL = 'http://localhost:5561'
        EVENTSTREAM_ALLOW_ORIGIN = "http://127.0.0.1:8000"

* Add url pattern for SSE channels 
  
        dashboard_channels = []  # per dashboard, per component etc
        urlpatterns += [path('events/', include(django_eventstream.urls), {"channels": dashboard_channels})]    

* Refer to django_eventstream regarding authentication
* You will also need to deploy a pushpin instance or use Fanout Cloud. 
* This is posting all events to test, you'd want to consider spreading events to different 
  channels for dashboards/components e.g. https://github.com/fanout/django-eventstream#routes-and-channel-selection 

