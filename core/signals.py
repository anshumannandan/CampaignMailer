from django.dispatch import receiver
from django.db.models.signals import post_save
from . models import Campaign
from . views import assign_task_to_celery

@receiver(post_save, sender=Campaign)
def set_default_username(sender, instance, created, **kwargs):
    if created and instance.schedule_for is not None: 
        assign_task_to_celery(instance, instance.schedule_for)