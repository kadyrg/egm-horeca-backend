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

X_FRAME_OPTIONS = "ALLOWALL"

SECRET_KEY = 'django-insecure-qopwi%4*rf!@%+4%3cs^c&!j%aanh8ac%hr@)*)s-y8y(ffjcg'

ALLOWED_HOSTS = [
    'egmhoreca.local',
    "egmhoreca-backend.egmhoreca.local",
    'admin.egmhoreca.ro',
    'egmhoreca.ro',
    'www.egmhoreca.ro',
    'localhost'
]

CSRF_TRUSTED_ORIGINS = [
    'https://egmhoreca.local',
    "https://backend.egmhoreca.local",
    'https://admin.egmhoreca.ro',
    'https://www.admin.egmhoreca.ro',
    'https://egmhoreca.ro',
    'https://www.egmhoreca.ro',
    'http://localhost:8000',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'banners',
    'categories',
    'products',
    'orders',
    'translations',
    'contacts',
    'legal'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://egmhoreca.local',
    "https://backend.egmhoreca.local",
    'https://admin.egmhoreca.ro',
    'https://www.admin.egmhoreca.ro',
    'https://egmhoreca.ro',
    'https://www.egmhoreca.ro',
    'http://localhost:8000',
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "egmhoreca-backend.renderers.CamelCaseJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}

ROOT_URLCONF = 'egmhoreca-backend.urls'

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

WSGI_APPLICATION = 'egmhoreca-backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASS"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),
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
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
