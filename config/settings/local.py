from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-dl@euiayq23c!hzvk@$p4sgz-*plxqrw4^n4drr+s*5ll1c8j#"


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "corporate-assets-tracker-local-db.sqlite3",
    }
}


# Email backend for development

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
