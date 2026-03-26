from django.db.models.signals import post_save
from django.dispatch import receiver
from items.models import Character
from dkp.models import DKPProfile


@receiver(post_save, sender=Character)
def create_dkp_profile(sender, instance, created, **kwargs):
    """Automatically create a DKPProfile whenever a new Character is created."""
    if created:
        DKPProfile.objects.get_or_create(character=instance)
