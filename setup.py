from os import path, linesep
from socket import gethostname
from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
secrets_file = 'config/settings/secrets.py'


if not path.isfile(secrets_file):
    allowed_host = input('Hostname (Empty=%s):%s' % (gethostname(), linesep))
    if not allowed_host:
        allowed_host = gethostname()

    with open(secrets_file, 'w') as f:
        f.write("__all__ = ['ALLOWED_HOSTS', 'SECRET_KEY']%s" %
                (linesep))

        f.write("ALLOWED_HOSTS = ['localhost', '%s']%s" %
                (allowed_host, linesep))

        f.write("SECRET_KEY = %s%s" %
                (get_random_string(50, chars), linesep))
