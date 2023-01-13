==========
Quickstart
==========

This is a quickstart guide for creating a simple pipeline.

Project Setup
-------------

Create a new Django project::

    # Create the project directory
    mkdir demo
    cd demo

    # Create a virtual environment
    pyenv virtualenv 3.11.0 django-wildcoeus-demo
    pyenv activate django-wildcoeus-demo

    # Install
    pip install django-wildcoeus

    # Set up a new project
    django-admin startproject demo .
    cd demo
    django-admin startapp mypipeline


Settings
========
Firstly we need to add :code:`wildcoeus`, :code:`wildcoeus.pipelines` and the new app :code:`demo.mypipeline` to :code:`INSTALLED_APPS` in :code:`demo/settings.py`::

    INSTALLED_APPS = [
        ...
        "django.contrib.humanize",
        "wildcoeus",
        "wildcoeus.pipelines",
        "demo.mypipeline",
    ]


Config
======
Then, in order to make pipelines discoverable we need to update :code:`demo/mypipeline/apps/py`::

    from django.apps import AppConfig

    class MypipelineConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'demo.mypipeline'

        def ready(self):
            from wildcoeus.pipelines.registry import pipeline_registry
            pipeline_registry.autodiscover()

Migrate
=======
Finally we sync the database by running::

    cd ..
    python manage.py migrate


Creating a Pipeline
-------------------

Now the project is setup we are ready to start building our first pipeline.
The first thing we need to do is setup a pipeline definition.

Create a new file :code:`demo/mypipeline/pipelines.py`

Note: It is important that you name the file :code:`pipelines.py` as this is used by the registry to discover your pipelines::

    from wildcoeus.pipelines import Pipeline, Task
    from wildcoeus.pipelines.registry import pipeline_registry


    class PrintWelcomeMessageTask(Task):
        title = "Print Welcome Message"

        def run(self, pipeline_id, run_id, cleaned_data):
            print("Hello World!")


    @pipeline_registry.register
    class FirstPipeline(Pipeline):
        print_message = PrintWelcomeMessageTask()

        class Meta:
            title = "First pipeline"

Here we are creating a pipline :code:`FirstPipeline` with one task :code:`print_message`.   Pipelines can
have multiple tasks and we will show this in the next section.

All Pipelines must be decorated with the
:code:`@pipeline_registry.register` decorator and inherit from the base class :code:`Pipeline`.

We have also defined our first task: :code:`PrintWelcomeMessageTask`.  Here we are just printing "Hello World!" but
can make this as complex as you require.  All tasks should inherit from :code:`Task` and have a :code:`run` method defined.

And we're done.

Running the pipeline
---------------------
The quickest way to run a pipeline for testing is by running the management command::

    python manage.py pipelines

After running this you should see a list of pipelines, numbered, and a prompt of 'Which pipelines would you like to start?'::

    Pipelines:
    1). demo.mypipeline.pipelines.FirstPipeline:

    Which pipelines would you like to start?

Type 1 to run FirstPipeline.  You will now be shown a list of tasks the pipeline will run along with a prompt for how you wish to run it::

    demo.mypipeline.pipelines.FirstPipeline will run the following tasks:
    1). print_message: Print Message

    Run [r], Run eager [e] or Cancel [c]?

You have the option to run the pipeline in eager mode or as a background task via Celery.
Since we have not set Celery up we will run it in Eager mode by typing e.  You should then see::

    Hello World!
    Pipeline Completed

As you can see the Hello World! message has been printed to the console just as we defined in the Task.

Adding another Task
===================

To complete this example we will add another task to our pipeline.  Update :code:`demo/mypipeline/pipelines.py`::

    import time
    from wildcoeus.pipelines import Pipeline, Task
    from wildcoeus.pipelines.registry import pipeline_registry


    class PrintWelcomeMessageTask(Task):
        title = "Print Welcome Message"

        def run(self, pipeline_id, run_id, cleaned_data):
            print("3 Times Table:")


    class PrintNumbersTask(Task):
        title = "Print 3 times table"

        def run(self, pipeline_id, run_id, cleaned_data):
            for i in range(1, 13):
                print(f"{i} x 3 = {i*3}")
                time.sleep(0.5)


    @pipeline_registry.register
    class FirstPipeline(Pipeline):
        print_message = PrintWelcomeMessageTask()
        numbers_task = PrintNumbersTask(config={"parents": ["print_message"]})

        class Meta:
            title = "First pipeline"

We have now defined a second task :code:`PrintNumbersTask` which prints the 3 times table from 1-12.
We also include a slight delay (0.5 seconds) between iterations so you can see it better when running the pipeline.

We have added this new task to our pipeline and specified that this should run after :code:`print_message` by adding
a config variable to the task instance :code:`config={"parents": ["print_message"]}`.  Adding this allows us to define
the exact order each task should be ran.

If we again run the pipeline using the management command we should now see::

    Pipelines:
    1). demo.mypipeline.pipelines.FirstPipeline:

    Which pipelines would you like to start? 1
    demo.mypipeline.pipelines.FirstPipeline will run the following tasks:
    1). print_message: Print Message
    2). numbers_task: Print 3 times table

    Run [r], Run eager [e] or Cancel [c]? e
    3 Times Table:
    1 x 1 = 3
    2 x 2 = 6
    3 x 3 = 9
    4 x 4 = 12
    5 x 5 = 15
    6 x 6 = 18
    7 x 7 = 21
    8 x 8 = 24
    9 x 9 = 27
    10 x 10 = 30
    11 x 11 = 33
    12 x 12 = 36
    Pipeline Completed


Monitoring Pipelines
====================

To wire up the pipeline monitoring views we need to add them to the urls file.  In :code:`demo/urls.py` add::

    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('pipelines/', include('wildcoeus.pipelines.urls')),
    ]


In order to view these pages you need to be logged in as a staff user.  So first lets create a superuser for our site::

    python manage.py createsuperuser

After completing this you will have an account setup with superuser access, so lets run our site::

    python manage.py runserver

We need to login before we can view any of the pipeline pages so navigate to http://127.0.0.1:8000/admin/ and login
using the details you entered when creating the superuser.

Once logged in you can access the pipeline monitoring pages at: http://127.0.0.1:8000/pipelines/

.. image:: _images/quickstart_pipelines.png
   :alt: Pipeline List

This list shows the each pipeline, how many tasks are associated with each, how may times it ran, including which
have passed and which have failed, when it was last ran, and the average amount of time it took to run.
You also have the option to run the pipeline.

If you click on the runs cell you will be taken to the pipeline execution page.

.. image:: _images/quickstart_pipeline_executions.png
   :alt: Pipeline Execution List

This shows details of each execution of the pipeline including: the pipeline and task count, when it was started,
how long it took to run and what was the status of the pipeline.

To see further details of a particular execution, click on the pipeline name.

.. image:: _images/quickstart_pipeline_results.png
   :alt: Pipeline Result Details

This details view shows a breakdown of each task which was ran including: the task name, status, and when it
started finished and duration.  You also have the option to rerun the individual task.

The logs recorded during the pipeline run is also shown on this page.  This can be useful if you are trying to
debug why a pipeline is not running correctly.