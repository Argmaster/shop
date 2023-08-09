"""Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Wrapper for configuration loaded from local storage."""

    model_config = SettingsConfigDict(env_prefix="")

    SECRET_KEY: str = Field(default="foo")
    """Django secret key value."""

    DEBUG: bool = Field(default=False)
    """Boolean indicating wether debug mode should be enabled."""

    DJANGO_ALLOWED_HOSTS: str = Field(default="")
    """Space separated list of allowed hosts."""

    SQL_ENGINE: str = Field(default="django.db.backends.sqlite3")

    SQL_DATABASE: str = Field(default=(BASE_DIR / "db.sqlite3").as_posix())

    SQL_USER: str = Field(default="user")

    SQL_PASSWORD: str = Field(default="password")

    SQL_HOST: str = Field(default="localhost")

    SQL_PORT: str = Field(default="5432")

    def get_allowed_hosts(self) -> list[str]:
        """Get allowed hosts as list."""
        return self.DJANGO_ALLOWED_HOSTS.split(" ")


local_settings = Settings()  # type: ignore[call-arg]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

ALLOWED_HOSTS: list[str] = local_settings.get_allowed_hosts()


# Application definition

INSTALLED_APPS = [
    "main.apps.MainConfig",
    "farm.apps.FarmConfig",
    "transactions.apps.TransactionsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "shop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": local_settings.SQL_ENGINE,
        "NAME": local_settings.SQL_DATABASE,
        "USER": local_settings.SQL_USER,
        "PASSWORD": local_settings.SQL_PASSWORD,
        "HOST": local_settings.SQL_HOST,
        "PORT": local_settings.SQL_PORT,
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_TRUSTED_ORIGINS = ["http://localhost:1337"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
