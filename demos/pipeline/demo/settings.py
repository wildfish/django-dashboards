from os import environ
from pathlib import Path

import envdir
from configurations import Configuration
from kombu import Queue

# Common settings
BASE_DIR = Path(__file__).absolute().parent.parent
PROJECT_NAME = "demo"
CONFIGURATION = environ["DJANGO_CONFIGURATION"]
CONFIG_DIR = environ.get("DJANGO_CONFIG_DIR")
SECRET_DIR = environ.get("DJANGO_SECRET_DIR")


def get_env(name, default=None, required=False, cast=str):
    """
    Get an environment variable
    Arguments:
        name (str): Name of environment variable
        default (Any): default value
        required (bool): If True, raises an ImproperlyConfigured error if not defined
        cast (Callable): function to call with extracted string value.
            Not applied to defaults.
    """

    def _lookup(self):
        value = environ.get(name)

        if value is None and default is not None:
            return default

        if value is None and required:
            raise ValueError(f"{name} not found in env")

        return cast(value)

    return property(_lookup)


def get_secret(name, cast=str):
    """
    Get a secret from disk
    Secrets should be available as the content of `<SECRET_DIR>/<name>`
    All secrets are required
    Arguments:
        name (str): Name of environment variable
        cast (Callable): function to call on extracted string value
    """

    # We don't want this to be called unless we're in a configuration which uses it
    def _lookup(self):
        if not SECRET_DIR:
            raise ValueError(
                f"Secret {name} not found: DJANGO_SECRET_DIR not set in env"
            )

        file = Path(SECRET_DIR) / name
        if not file.exists():
            raise ValueError(f"Secret {file} not found")

        value = file.read_text().strip()
        return cast(value)

    return property(_lookup)


def csv_to_list(value):
    """
    Convert a comma separated list of values into a list.
    Convenience function for use with get_env() and get_secret() ``cast`` argument.
    """
    if value is None:
        return []
    return value.split(",")


class Common(Configuration):
    @classmethod
    def pre_setup(cls):
        """
        If specified, add config dir to environment
        """
        if CONFIG_DIR:
            envdir.Env(CONFIG_DIR)
        super().pre_setup()

    PROJECT_ENVIRONMENT_SLUG = f"{PROJECT_NAME}_{CONFIGURATION}".lower()

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
    SECRET_KEY = get_env("DJANGO_SECRET_KEY", PROJECT_NAME)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", cast=csv_to_list, default=["*"])

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

    # # Celery
    # CELERY_REDIS_HOST = get_env("CELERY_REDIS_HOST", default="redis")
    # CELERY_REDIS_PORT = get_env("CELERY_REDIS_PORT", default=6379, cast=int)
    # CELERY_REDIS_BROKER_DB = get_env("CELERY_REDIS_BROKER_DB", default=1, cast=int)
    #
    # CELERY_RESULT_BACKEND = "django-db"
    # CELERY_BROKER_CONNECTION_MAX_RETRIES = 1
    # CELERY_TASK_MAX_RETRIES = 1
    #
    # @property
    # def CELERY_BROKER_URL(self):
    #     return f"redis://{self.CELERY_REDIS_HOST}:{self.CELERY_REDIS_PORT}/{self.CELERY_REDIS_BROKER_DB}"

    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    DATABASE_HOST = get_env("DATABASE_HOST", default="localhost")
    DATABASE_PORT = get_env("DATABASE_PORT", default=5432, cast=int)
    DATABASE_NAME = get_env("DATABASE_NAME", default=PROJECT_NAME)
    DATABASE_USER = get_env("DATABASE_USER", default=PROJECT_NAME)
    DATABASE_PASSWORD = get_env("DATABASE_PASSWORD", default=PROJECT_NAME)

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

    CORS_ALLOW_ALL_ORIGINS = True

    GRIP_URL = "http://localhost:5561"
    EVENTSTREAM_ALLOW_ORIGIN = "http://127.0.0.1:8000"
    EVENTSTREAM_ALLOW_CREDENTIALS = True
    EVENTSTREAM_ALLOW_HEADERS = "Authorization"

    WILDCOEUS_PIPELINE_RUNNER = "wildcoeus.pipelines.runners.celery.runner.Runner"


class RedisCache:
    REDIS_HOST = get_env("DJANGO_REDIS_HOST", required=True)
    REDIS_PORT = get_env("DJANGO_REDIS_PORT", default=6379, cast=int)

    REDIS_DB_CACHE = "1"
    REDIS_DB_CACHEOPS = "2"
    REDIS_DB_CELERY_QUEUE = "3"
    REDIS_DB_CELERY_RESULTS = "4"
    REDIS_DB_TASK_KEYS = "5"

    REDIS_PROTOCOL = get_env("REDIS_PROTOCOL", default="redis")

    REDIS_LOCATION = f"{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}"
    REDIS_LOCATION = "redis://redis:6379"

    # Cache
    # https://docs.djangoproject.com/en/3.0/ref/settings/#caches
    @property
    def CACHES(self):
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": f"{self.REDIS_LOCATION}/{self.REDIS_DB_CACHE}",
                "KEY_PREFIX": f"{self.PROJECT_ENVIRONMENT_SLUG}_",
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

    # CELERY_BEAT_SCHEDULE = {}

    CELERY_TASK_QUEUES = (
        Queue(CELERY_TASK_DEFAULT_QUEUE, routing_key=CELERY_TASK_DEFAULT_QUEUE),
        Queue(CELERY_TASK_PROCESSING_QUEUE, routing_key=CELERY_TASK_PROCESSING_QUEUE),
        Queue(CELERY_TASK_HIGHIO_QUEUE, routing_key=CELERY_TASK_HIGHIO_QUEUE),
    )


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


class DevDocker(RedisCache, Dev):
    """
    Dev for docker, uses Redis.
    """


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


class Deployed(RedisCache, Common):
    """
    Settings which are for a non-local deployment
    """

    # Redefine values which are not optional in a deployed environment
    ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", cast=csv_to_list, required=True)

    # Some deployed settings are no longer env vars - collect from the secret store
    SECRET_KEY = get_secret("DJANGO_SECRET_KEY")
    DATABASE_USER = get_secret("DATABASE_USER")
    DATABASE_PASSWORD = get_secret("DATABASE_PASSWORD")

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


class Stage(Deployed):
    pass


class Prod(Deployed):
    DEBUG = False
