import os
from os import environ
from pathlib import Path

import envdir
from configurations import Configuration
from kombu import Queue


# Common settings
BASE_DIR = Path(__file__).absolute().parent.parent
PROJECT_NAME = "demo"
CONFIGURATION = environ["DJANGO_CONFIGURATION"]
_lower_django_configuration = CONFIGURATION.lower()
CONFIG_DIR = environ.get("DJANGO_CONFIG_DIR")
SECRET_DIR = environ.get("DJANGO_SECRET_DIR")


def get_env_variable(var_name, default=None, prefix="DJANGO"):
    """Get the environment variable or return exception."""

    # TODO The exception is not displayed on the console if the env variable
    # is not set and there is no default.
    if prefix:
        var_name = f"{prefix}_{var_name}"
    if default is not None:
        return os.environ.get(var_name, default)
    else:
        try:
            return os.environ[var_name]
        except KeyError:
            error_msg = "Set the {} environment variable".format(var_name)
            print(error_msg)


def get_env_boolean(var_name, default=None, prefix="DJANGO"):
    value = get_env_variable(var_name, default, prefix=prefix)
    if isinstance(value, str) and value.lower() in ["false", "0"]:
        return False
    else:
        return bool(value)


class Common(Configuration):
    @property
    def ADMINS(self):
        """
        Look up DJANGO_ADMINS and split into list of (name, email) tuples
        Separate name and email with commas, name+email pairs with semicolons, eg::
            DJANGO_ADMINS="User One,user1@example.com;User Two,user2@example.com"
        """
        value = environ.get("DJANGO_ADMINS")
        if not value:
            return []

        pairs = value.split(";")
        return [pair.rsplit(",", 1) for pair in pairs]

    MANAGERS = ADMINS

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = get_env_variable("SECRET_KEY", PROJECT_NAME)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    INSTALLED_APPS = [
        # Django
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.humanize",
        # Third party
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "django_extensions",
        # "django_celery_results",
        # pipelines
        "wildcoeus",
        "wildcoeus.pipelines",
        # Project
        "demo.basic.apps.BasicConfig",
    ]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "demo.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                BASE_DIR / "templates",
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "demo.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    DATABASE_HOST = get_env_variable("DB_HOST", default="localhost")
    DATABASE_PORT = int(get_env_variable("DB_PORT", default=5432))
    DATABASE_NAME = get_env_variable("DB_NAME", default=PROJECT_NAME)
    DATABASE_USER = get_env_variable("DB_USERNAME", default=PROJECT_NAME)
    DATABASE_PASSWORD = get_env_variable("DB_PASSWORD", default=PROJECT_NAME)

    @property
    def DATABASES(self):
        """
        Build the databases object here to allow subclasses to override specific values
        """
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "HOST": self.DATABASE_HOST,
                "PORT": self.DATABASE_PORT,
                "NAME": self.DATABASE_NAME,
                "USER": self.DATABASE_USER,
                "PASSWORD": self.DATABASE_PASSWORD,
            }
        }

    # Password validation
    # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.0/topics/i18n/
    LANGUAGE_CODE = "en-GB"

    TIME_ZONE = "Europe/London"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "static"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

    # Additional locations of static files
    STATICFILES_DIRS = [BASE_DIR / "frontend" / "dist"]

    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_ROOT = BASE_DIR / "public"

    FIXTURE_DIRS = [BASE_DIR / "fixtures"]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "wildcoeus-pipelines": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    # redis

    REDIS_DB_CACHE = "1"
    REDIS_DB_CACHEOPS = "2"
    REDIS_DB_CELERY_QUEUE = "3"
    REDIS_DB_CELERY_RESULTS = "4"
    REDIS_DB_TASK_KEYS = "5"

    REDIS_HOST = get_env_variable("REDIS_HOST", default="redis")
    REDIS_PORT = get_env_variable("REDIS_PORT", default="6379")
    REDIS_PROTOCOL = get_env_variable("REDIS_PROTOCOL", default="redis")

    REDIS_LOCATION = f"{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}"

    # Caching

    # Cache
    # https://docs.djangoproject.com/en/3.0/ref/settings/#caches
    @property
    def CACHES(self):
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": f"{self.REDIS_LOCATION}/{self.REDIS_DB_CACHE}",
                "KEY_PREFIX": "{}_".format(_lower_django_configuration),
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    "PARSER_CLASS": "redis.connection.HiredisParser",
                },
            }
        }

    # celery

    CELERY_BROKER_URL = f"{REDIS_LOCATION}/{REDIS_DB_CELERY_QUEUE}"
    CELERY_TASK_KEYS_URL = f"{REDIS_LOCATION}/{REDIS_DB_TASK_KEYS}"
    CELERY_RESULT_BACKEND = f"{REDIS_LOCATION}/{REDIS_DB_CELERY_RESULTS}"
    CELERY_RESULT_EXPIRES = 1800  # 30m
    CELERY_RESULT_COMPRESSION = "gzip"
    CELERY_TASK_COMPRESSION = "gzip"

    REDBEAT_LOCK_TIMEOUT = 600  # 10 minutes

    CELERY_TASK_DEFAULT_QUEUE = "default"
    CELERY_TASK_PROCESSING_QUEUE = "processing"
    CELERY_TASK_HIGHIO_QUEUE = "highio"
    # CELERY_TASK_ALWAYS_EAGER = True

    # CELERY_BEAT_SCHEDULE = {}

    CELERY_TASK_QUEUES = (
        Queue(CELERY_TASK_DEFAULT_QUEUE, routing_key=CELERY_TASK_DEFAULT_QUEUE),
        Queue(CELERY_TASK_PROCESSING_QUEUE, routing_key=CELERY_TASK_PROCESSING_QUEUE),
        Queue(CELERY_TASK_HIGHIO_QUEUE, routing_key=CELERY_TASK_HIGHIO_QUEUE),
    )

    WILDCOEUS_PIPELINE_RUNNER = "wildcoeus.pipelines.runners.celery.runner.Runner"
    # WILDCOEUS_PIPELINE_RUNNER = "wildcoeus.pipelines.runners.eager.Runner"
    WILDCOEUS_PIPELINE_REPORTER = "wildcoeus.pipelines.reporters.orm.ORMReporter"


class Dev(Common):
    DEBUG = True
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = "/tmp/app-emails"
    INTERNAL_IPS = ["127.0.0.1"]
    ENABLE_SILK = True

    @property
    def INSTALLED_APPS(self):
        INSTALLED_APPS = super().INSTALLED_APPS
        INSTALLED_APPS.append("silk")
        return INSTALLED_APPS

    @property
    def MIDDLEWARE(self):
        MIDDLEWARE = super().MIDDLEWARE
        MIDDLEWARE.append("silk.middleware.SilkyMiddleware")
        return MIDDLEWARE


class Test(Common):
    """
    Default test settings

    Includes some testing speedups.
    """

    DEBUG = False
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


class CI(Test):
    """
    Default CI settings
    """


class Deployed(Common):
    """
    Settings which are for a non-local deployment
    """

    DEBUG = False
    DJANGO_VITE_DEV_MODE = False

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

    ENABLE_SILK = False

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    DEFAULT_FROM_EMAIL = ""
    SERVER_EMAIL = ""

    ALLOWED_HOSTS = [get_env_variable("ALLOWED_HOSTS")]

    @classmethod
    def post_setup(cls):
        super(Deployed, cls).post_setup()
        if cls.SENTRY_ENABLED:
            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                integrations=[
                    DjangoIntegration(),
                    RedisIntegration(),
                ],
                send_default_pii=True,
                environment=_lower_django_configuration,
                # glitchtip doesn't really support sampling, disabled for now.
                traces_sample_rate=0,
            )
