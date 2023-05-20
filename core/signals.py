from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from . models import User, Campaign
from . views import assign_task_to_celery
from django.core.exceptions import ValidationError


@receiver(pre_save, sender=User)
def check_unique_email(sender, instance, **kwargs):
    if instance.pk is None and User.objects.filter(email=instance.email).exists():
        raise ValidationError("Email already in use")


@receiver(post_save, sender=Campaign)
def set_default_username(sender, instance, created, **kwargs):
    if created and instance.schedule_for is not None: 
        assign_task_to_celery(instance, instance.schedule_for)