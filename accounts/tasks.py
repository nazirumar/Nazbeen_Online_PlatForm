# accounts/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from accounts.models import CustomUser
from .utils import generate_token

@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_activation_email(self, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        subject = "Activate Your Account"
        message = render_to_string('accounts/activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',  # Update this to your production domain
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except CustomUser.DoesNotExist:
        # Log or handle user not found
        pass
    except Exception as exc:
        raise self.retry(exc=exc)  # Retry the task if there's an error
