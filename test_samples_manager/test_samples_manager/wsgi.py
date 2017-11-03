"""
WSGI config for test_samples_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR']))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_samples_manager.settings")


from django.core.wsgi import get_wsgi_application



application = get_wsgi_application()
