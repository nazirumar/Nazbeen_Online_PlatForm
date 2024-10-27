from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
import logging
from .utils import account_activation_token

User = get_user_model()

logger = logging.getLogger(__name__)

def send_activation_email(user):
    """
    Sends an activation email to the user.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)  # Remove the trailing comma
    subject = "Activate Your Account"
    activation_link = f"{settings.SITE_DOMAIN}{reverse('activate', kwargs={'uidb64': uidb64, 'token': token})}"
    message = render_to_string('accounts/account_activation_email.html', {
        'user': user,
        'domain': settings.SITE_DOMAIN,  # Ensure SITE_DOMAIN is set in settings
        'activation_link': activation_link,
    })

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=message,  # Use HTML template for email content

        )
        logger.info(f"Activation email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send activation email to {user.email}: {e}")

@shared_task
def send_activation_email_task(user_id):
    """
    Celery task to send an activation email to a user by user_id.
    """
    try:
        user = User.objects.get(id=user_id)
        send_activation_email(user)
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist")



@shared_task
def send_password_reset_email(user_id, domain, protocol='http'):
    """
    Task to send a password reset email to the user with user_id.
    """
    try:
        user = User.objects.get(pk=user_id)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})}"
        
        subject = "Password Reset Request"
        message = render_to_string('accounts/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=message,
        )
    except User.DoesNotExist:
        pass
