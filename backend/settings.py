from pathlib import Path
from decouple import Config,  RepositoryEnv


BASE_DIR = Path(__file__).resolve().parent.parent

env_file = BASE_DIR / ".env.development"
config = Config(RepositoryEnv(env_file))

ENV = config("ENV")
DEBUG = config("DEBUG", cast=bool)
REVALIDATE_API = config("REVALIDATE_API")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")

SECRET_KEY = 'django-insecure-qopwi%4*rf!@%+4%3cs^c&!j%aanh8ac%hr@)*)s-y8y(ffjcg'

ALLOWED_HOSTS = [
    "backend.egmhoreca.local",
    'localhost',
    '176.223.120.224/',
]

CSRF_TRUSTED_ORIGINS = [
    "https://backend.egmhoreca.local",
    'http://localhost:8000',
    'http://176.223.120.224/'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'banners',
    'categories',
    'products',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "backend.renderers.CamelCaseJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'egmhoreca',
        'USER': 'avnadmin',
        'PASSWORD': config("DB_PASS"),
        'HOST': 'delivery-kadyr-d419.l.aivencloud.com',
        'PORT': '10201',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
