# your_project/__init__.py
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared tasks will use it.
from .celery import app as celery_app

__all__ = ('celery_app',)
