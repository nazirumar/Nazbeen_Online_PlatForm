from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProfileUser
User = get_user_model()


@receiver(post_save, sender=User)
def create_staff_for_new_user(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)