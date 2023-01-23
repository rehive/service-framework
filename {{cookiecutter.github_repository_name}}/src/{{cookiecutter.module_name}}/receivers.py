from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from {{cookiecutter.module_name}}.models import Currency


@receiver(post_save, sender=Currency)
def set_manager(sender, instance, created, **kwargs):
    if (instance.wyre_code != instance._original_wyre_code):
        # Set as the manager on Rehive for the currency
        instance.set_as_rehive_manager()