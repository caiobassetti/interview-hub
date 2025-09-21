from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Email to console is fine for dev
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
