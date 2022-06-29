# flake8: noqa

from .base import *

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("KOK_DATABASE_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "HOST": os.environ.get("KOK_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("KOK_DATABASE_PORT", "5432"),
        "NAME": os.environ.get("KOK_DATABASE_NAME", "kokalamzorlashtirish"),
        "USER": os.environ.get("KOK_DATABASE_USER", "kokalamzorlashtirish"),
        "PASSWORD": os.environ.get("KOK_DATABASE_PASSWORD", ""),
    }
}