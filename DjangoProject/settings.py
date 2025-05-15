import os
from pathlib import Path

# ── Build paths inside the project ─────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── SECURITY ────────────────────────────────────────────────
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-@z$q375ar)y0j^@_$=o%u5g-q+11y%)kz7k2^zr)l_&k$7zedp')
DEBUG      = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'cbuettner.pythonanywhere.com',
]

# ── Applications ────────────────────────────────────────────
INSTALLED_APPS = [
    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Billing
    'billing',

    # django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Payments
    'payments',

    # Your apps
    'accounts',
    'products',
    'cart',
    'orders',
]

SITE_ID = 1

# ── Middleware & URL config ─────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject.wsgi.application'

# ── Database ────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── Password validation ────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'

# ── Internationalization ──────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/Chicago'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

# ── Static & media files ──────────────────────────────────
STATIC_URL          = '/static/'
STATICFILES_DIRS    = [BASE_DIR / 'static']
STATIC_ROOT         = BASE_DIR / 'staticfiles'

MEDIA_URL           = '/media/'
MEDIA_ROOT          = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Cart session key ───────────────────────────────────────
CART_SESSION_ID = 'cart'

# ── EMAIL (real SMTP backend) ─────────────────────────────
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = os.getenv('EMAIL_HOST',       'smtp.gmail.com')
EMAIL_PORT          = int(os.getenv('EMAIL_PORT',   '587'))
EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS',    'True') == 'True'
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')      # e.g. you@gmail.com
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # your SMTP/App password
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER

# ── Payments dummy gateway (all environments) ────────────
PAYMENT_HOST = 'localhost:8000'
PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {}),
}


