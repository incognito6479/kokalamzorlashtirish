# flake8: noqa

from .base import *

DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "PROJECT_DATABASE_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "HOST": os.environ.get("PROJECT_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("PROJECT_DATABASE_PORT", "5432"),
        "NAME": os.environ.get("PROJECT_POSTGRES_DB", "landscaping"),
        "USER": os.environ.get("PROJECT_POSTGRES_USER", "landscaping"),
        "PASSWORD": os.environ.get("PROJECT_POSTGRES_PASSWORD", "landscaping"),
    }
}

ALLOWED_HOSTS = [
    "158.8.212.75",
    "pitomnik.novalab.uz",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]
INSTALLED_APPS += ["django_extensions"]
