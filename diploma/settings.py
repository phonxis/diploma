"""
Django settings for diploma project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ckwliq4(n2v5da91bmtt(b@*yopp1%!$e@_rf5(rq@+mpzmosb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'embed_video',
    #'memcache_status',

    # myapps
    'courses',
    'students',

    # должно быть после myapps, что бы отображался кастомный
    # logout template вместо logout template из админки
    'django.contrib.admin',

    # social auth
    #'social.apps.django_app.default',
    'social_django',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # social auth
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'diploma.urls'

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

                # social auth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'diploma.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'teauolye',
        #'USER': 'teauolye',
        #'PASSWORD': '_-yfBiO6L0nTk-yxb_tutGpwpBw2Pg78',
        #'HOST': '',
        #'PORT': ''
    }
}

import dj_database_url
DATABASES['default'] = dj_database_url.parse(
    # elephantSQL
    #'postgres://teauolye:_-yfBiO6L0nTk-yxb_tutGpwpBw2Pg78@horton.elephantsql.com:5432/teauolye',

    #heroku
    'postgres://gnkcqpkozlozbd:95ef32cee05885fb26001750cf4b8199a7b11f1b48eae07f55e7a9750696c9d9@ec2-54-75-237-110.eu-west-1.compute.amazonaws.com:5432/d82d04ff8cjqa5',
    conn_max_age=600
)


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


from django.core.urlresolvers import reverse_lazy
# куда будут перенаправлены студенты после аутентификации
#LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'


# CACHE
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}


AUTHENTICATION_BACKENDS = (
    #'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',

    'students.auth_backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',

    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '85228042737-bm10of2jf7r4ti5d60c4ddbaovdf7s2f.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'znVv5zyLysvpzL5wvyK5O5D1'

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'ru_RU',
    'fields': 'id, name, email, picture',
}
SOCIAL_AUTH_FACEBOOK_KEY = '591899737662437'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b8156b6c16875cd7596c7c48f33dbc27'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_VK_OAUTH2_KEY = '5125866'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'KJ0h54VKKNfd9FDBK9Zo'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['photo_200_orig']
SOCIAL_AUTH_VK_OAUTH2_API_VERSION = '5.5'

#SOCIAL_AUTH_GITHUB_KEY = ''
#SOCIAL_AUTH_GITHUB_SECRET = ''
#SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

