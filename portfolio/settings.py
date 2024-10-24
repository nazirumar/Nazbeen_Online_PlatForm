"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", cast=bool)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST", cast=str, default=None)
EMAIL_PORT = config("EMAIL_PORT", cast=str, default="587")  # Recommended
EMAIL_ADDRESS = "nazirumar888@gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
EMAIL_USE_TLS = config(
    "EMAIL_USE_TLS", cast=bool, default=True
)  # Use EMAIL_PORT 587 for TLS

ADMIN_USER_NAME = config("ADMIN_USER_NAME", default="Admin user")
ADMIN_USER_EMAIL = config("ADMIN_USER_EMAIL", default=None)

MANAGERS = []
ADMINS = []
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS += [(f"{ADMIN_USER_NAME}", f"{ADMIN_USER_EMAIL}")]
    MANAGERS = ADMINS


ALLOWED_HOSTS = [".saas-foundation-by-nazbeen.onrender.com"]
if DEBUG:
    ALLOWED_HOSTS.append("localhost")
    ALLOWED_HOSTS.append("127.0.0.1")
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_htmx",
    "embed_video",
    "redisboard",
    # 'daphne',
    'channels',

    # apps
    "accounts",
    "commando",
    "courses",
    "profiles",
    "instructors",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "courses.context_processors.category",
                "courses.context_processors.instructor_tag",


            ],
        },
    },
]

# Configure ASGI for Channels
WSGI_APPLICATION = "portfolio.wsgi.application"
ASGI_APPLICATION = 'portfolio.asgi.application'

# Channel layers configuration (using in-memory for local development)
# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}





# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("SQL_DATABASE", default=str(BASE_DIR / "db.sqlite3")),
        "USER": config("SQL_USER", default="user"),
        "PASSWORD": config("SQL_PASSWORD", default="password"),
        "HOST": config("SQL_HOST", default="localhost"),
        "PORT": config("SQL_PORT", default="5432"),
    }
}


CONN_MAX_AGE = config("CONN_MAX_AGE", cast=int, default=300)
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL is not None:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL, conn_max_age=CONN_MAX_AGE, conn_health_checks=True
        )
    }

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Ensure Redis is configured in your cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# settings.py
SESSION_COOKIE_SECURE = True  # Use HTTPS in production
CSRF_COOKIE_SECURE = True  # CSRF over HTTPS only
SESSION_COOKIE_HTTPONLY = True  # Prevent access via JavaScript


DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB limit, adjust as needed


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = LOGIN_URL

# Celery Configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Assuming Redis is running on localhost
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"


MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"


STATICFILES_BASE_DIR = BASE_DIR / "staticfiles"
STATICFILES_BASE_DIR.mkdir(exist_ok=True, parents=True)
STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / "vendors"

STATICFILES_DIRS = [STATICFILES_BASE_DIR]

STATIC_ROOT = BASE_DIR / "local-cdn"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# cloudinary video config
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_PUBLIC_API_KEY = config("CLOUDINARY_PUBLIC_API_KEY", default="")
CLOUDINARY_SECRET_API_KEY = config("CLOUDINARY_SECRET_API_KEY")
