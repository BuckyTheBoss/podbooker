import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Secret_Key_Here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'spoofed-domain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = 'FACEBOOK_KEY'
SOCIAL_AUTH_FACEBOOK_SECRET = 'FACEBOOK_SECRET'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','first_name','last_name' ]

LISTENNOTES_API_KEY = 'api_key'

# MailJet keys
MJ_APIKEY_PUBLIC  = 'api_key'
MJ_APIKEY_PRIVATE = 'api_key_private'
MJ_SENDER_EMAIL = 'sender_email'