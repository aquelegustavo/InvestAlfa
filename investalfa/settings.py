"""
Configurações do Django para o projeto

Para mais informações acesse:
https://docs.djangoproject.com/en/4.1/topics/settings/


"""

import os
import environ
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
""" Variáveis de ambiente """

SECRET_KEY = env("SECRET_KEY")
""" Secret da aplicação """

DEBUG = env("DEBUG") or False
""" Aplicação em depuração? """

ALLOWED_HOSTS = []
""" Hosts autorizados """

AUTH_USER_MODEL = 'users.CustomUser'
""" Usuário padrão """

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'investalfa.apps.companies',
    'investalfa.apps.monitoring',
    'investalfa.apps.quotes',
    'investalfa.apps.users',
]
""" Aplicativos intalados"""

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}
""" Configurações do Django Rest Framework """

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD': 'uid',
    'USER_ID_CLAIM': 'uid',
    'UPDATE_LAST_LOGIN': True,
}
""" Configurações do Django Rest Framework JWT """


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
""" Configurações de Middleware padrão """


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'investalfa', 'client', 'build')],
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
""" Configurações padrão de templates """

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(
    BASE_DIR, 'investalfa', 'client', 'build', 'static')]
""" 
Arquivos estáticos 

Static files (CSS, JavaScript, Images)
https://docs.djangoproject.com/en/4.1/howto/static-files/

"""

WSGI_APPLICATION = 'investalfa.wsgi.application'
""" Configuração WSGI """

ROOT_URLCONF = 'investalfa.urls'
""" Configurações de rotas """


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
""" 
Configuração padrão do database 

Para fins de demonstração e desenvolvimento, usando SQL lite
"""

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""" Chave primária padrão """


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
""" 
Validador de senha 

Saiba mais: https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
"""


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
""" Lingua da aplicação """

TIME_ZONE = 'UTC'
""" Horário Padrão da aplicação """

USE_I18N = True
""" Usar internacionalização """

USE_TZ = True
""" Usar Timezone """


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'inoamecontrata@gmail.com'
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'inoamecontrata@gmail.com'
""" Definições do client de email """
