import os
import sys
from pathlib import Path

# =========================================================================
# 👑 BASE DIRECTORY LAYOUT AND ENVIRONMENT FRAMEWORK DETECTION
# =========================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-getsemani-choir-portal-2026-auth-token-key')

DEBUG = False

ALLOWED_HOSTS = ['*', '.onrender.com']

# =========================================================================
# 👑 DATABASE ADAPTER INTEGRATION MATRIX (MOCKING PSYCOPG2 TO PREVENT CRASH)
# =========================================================================
try:
    import pg8000
    pg8000.paramstyle = 'format'
    pg8000.__version__ = "2.9.9"
    
    import types
    fake_errors = types.ModuleType('errors')
    fake_sql = types.ModuleType('sql')
    
    pg8000.errors = fake_errors
    pg8000.sql = fake_sql
    
    sys.modules['psycopg2'] = pg8000
    sys.modules['psycopg2.extensions'] = pg8000
    sys.modules['psycopg2.extras'] = pg8000
    sys.modules['psycopg2.errors'] = fake_errors
    sys.modules['psycopg2.sql'] = fake_sql
    
    pg8000.extensions = pg8000
    pg8000.extras = pg8000
except (ImportError, AttributeError, NameError, KeyError):
    pass

# =========================================================================
# 🗄️ PRODUCTION DATABASE ENGINE CONFIGURATION (PERMANENT SUPABASE CLUSTER)
# =========================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.tsnnlhgpwqwtertchoal',
        'PASSWORD': 'Getseman!2026',
        'HOST': '://supabase.com',
        'PORT': '5432',
    }
}

# =========================================================================
# ⚙️ APPLICATION MODULE DEFINITIONS LAYER
# =========================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'choir_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'choir_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'choir_config.wsgi:application'

# =========================================================================
# 🔒 SECURITY AND PASSWORD VALIDATION STANDARD RULES
# =========================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kigali'
USE_I18N = True
USE_TZ = True

# =========================================================================
# 🎨 STATIC FILES MINIFICATION CONFIGURATION (WHITENOISE ASSET ENGINE)
# =========================================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
