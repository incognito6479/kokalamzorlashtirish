import os

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "PROJECT_DATABASE_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "HOST": os.environ.get("PROJECT_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("PROJECT_DATABASE_PORT", "5432"),
        "NAME": os.environ.get("PROJECT_POSTGRES_DB", "test"),
        "USER": os.environ.get("PROJECT_POSTGRES_USER", "landscaping"),
        "PASSWORD": os.environ.get("PROJECT_POSTGRES_PASSWORD", "landscaping"),
    }
}
