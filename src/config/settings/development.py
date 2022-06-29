# flake8: noqa

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

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


        # "HOST": os.environ.get("PROJECT_DATABASE_HOST", "127.0.0.1"),
        # "PORT": os.environ.get("PROJECT_DATABASE_PORT", "5432"),
        # "NAME": os.environ.get("PROJECT_POSTGRES_DB", "landscaping"),
        # "USER": os.environ.get("PROJECT_POSTGRES_USER", "shaxbozaka"),
        # "PASSWORD": os.environ.get("PROJECT_POSTGRES_PASSWORD", "Shakhboz11"),


        # 'HOST': '127.0.0.1',
        # 'NAME': 'landscaping',
        # 'USER': 'postgres',
        # 'PASSWORD': '1357908642Bk_.A',

    }
}
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)
