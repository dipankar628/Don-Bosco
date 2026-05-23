"""
Django settings for St. Xavier's School, Harmutty website.

A Don Bosco Institution - CBSE Affiliation No: 230010
Email: saxaha@gmail.com | Phone: 9181533805, 03752-291165

This settings file is configured for development. For production deployment,
update SECRET_KEY, set DEBUG=False, and configure ALLOWED_HOSTS appropriately.
"""

import os
from pathlib import Path

# =============================================================================
# BASE DIRECTORY
# =============================================================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
# SECURITY WARNING: keep the secret key used in production secret!
# Generate a new one for production using: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'django-insecure-sx@v13rs-h@rmutty-d0n-b0sc0-2025-cbse230010-dev-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# In production, replace with your actual domain name(s)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','192.168.0.156', '.vercel.app']

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',          # Admin panel for notice management
    'django.contrib.auth',           # Authentication framework
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file serving

    # School website app
    'school_app',                    # Primary app with models, views, templates
]

# =============================================================================
# MIDDLEWARE
# =============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Visit counter - tracks every page load
    'school_app.middleware.VisitCounterMiddleware',
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================
ROOT_URLCONF = 'school_project.urls'

# =============================================================================
# TEMPLATE CONFIGURATION
# =============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django will look for templates in each app's templates/ directory
        'DIRS': [],
        'APP_DIRS': True,  # Enable template loading from app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Visit counter - provides today_visits & total_visits to all templates
                'school_app.context_processors.visit_counts',
            ],
        },
    },
]

# =============================================================================
# WSGI APPLICATION
# =============================================================================
WSGI_APPLICATION = 'school_project.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# Using SQLite for simplicity - perfect for a school website
# No additional database server installation required
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Indian Standard Time for Assam
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# =============================================================================
# URL prefix for static files
STATIC_URL = '/static/'

# Directory where collectstatic will gather all static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# =============================================================================
# MEDIA FILES (User-uploaded files like notice PDFs)
# =============================================================================
# URL prefix for media files
MEDIA_URL = '/media/'

# Directory where uploaded files (notice PDFs) will be stored
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
