import os
from . import private_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

SECRET_KEY = private_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['139.59.139.209','righi-network.com', 'www.righi-network.com', '127.0.0.1']

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'bootstrap_themes',
	'crispy_forms',
	'django_bootstrap_breadcrumbs',
	'chartit',
	'django_tables2',
	'markdown_deux',
	'pagedown',

	'accounts',
	'assemblee',
	'bilancio',
	'comments',
	'password_reset',
	'posts',
	'recuperi',
	'times',
	'tutoring',
]

SITE_ID = 1

MIDDLEWARE = [
	'django.middleware.locale.LocaleMiddleware',

	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'righinetwork.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],

		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
			'loaders': [
				('django.template.loaders.cached.Loader', (
					'django.template.loaders.filesystem.Loader',
					'django.template.loaders.app_directories.Loader',
				)),
			],
		},
	},
]

CRISPY_FAIL_SILENTLY = not DEBUG
# AUTHENTICATION_BACKENDS = (
# 	# Needed to login by username in Django admin, regardless of `allauth`
# 	'django.contrib.auth.backends.ModelBackend',
#
# 	# `allauth` specific authentication methods, such as login by e-mail
# 	'allauth.account.auth_backends.AuthenticationBackend',
# )

WSGI_APPLICATION = 'righinetwork.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'noreply@righi-network.com'
EMAIL_HOST_PASSWORD = private_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@righi-network.com'

LANGUAGE_CODE = 'it'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
	# '/home/leo/righinetwork/righinetwork/static/',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

# Django allauth

# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True
# # ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_FORMS = {'signup': 'accounts.forms.UserRegisterForm', 'login': 'accounts.forms.UserLoginForm'}
# ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
# LOGIN_REDIRECT_URL = '/'
