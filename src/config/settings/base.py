import os
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "*ixpi$8@z7_r%2z-xidbuxu5=hjxq2x^32ua+m=k+otmx1=+c6"


ALLOWED_HOSTS = ["0.0.0.0", "192.168.1.113", "127.0.0.1"]


BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]
LOCAL_APPS = [
    "account",
    "regionroad",
    "pitomnik",
    "vehicles",
    "accounting",
    "production",
    "archive",
]

THIRD_PARTY_APPS = [
    "phonenumber_field",
    "crispy_forms",
    "django_filters",
    "mathfilters"
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_PARTY_APPS
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "assets")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
AUTH_USER_MODEL = "account.User"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
# paginations
IRRIGATION_PAGE_SIZE = 10
IRRIGATION_TYPE_PAGE_SIZE = 10
PITOMNIK_PLANTS_PAGE_SIZE = 10
PLANTED_PLANTS_PAGE_SIZE = 10
PLANT_PAGE_SIZE = 10
PITOMNIK_PAGE_SIZE = 10
PLANT_TYPE_PAGE_SIZE = 10
SAVING_JOB_PAGE_SIZE = 10
VEHICLE_PAGE_SIZE = 20
USER_PAGE_SIZE = 10
ORGANIZATION_PAGE_SIZE = 20
DISTRICT_ROAD_PAGE_SIZE = 20
NEW_IRRIGATION_PAGE_SIZE = 10
DEBIT_CREDIT_PAGE_SIZE = 20
PITOMNIK_SAVING_JOB_PAGE_SIZE = 20

LOGIN_URL = reverse_lazy("account:login")
LOGIN_REDIRECT_URL = "pitomnik/map"
CRISPY_TEMPLATE_PACK = "bootstrap4"
