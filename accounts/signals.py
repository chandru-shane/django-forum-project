from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from profiles.models import UserProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(
            user=instance, display_name=instance.username
        )
        profile.save()
