from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from openapi_documentor.openapi.models import Document
from .models import User

@receiver(post_save, sender=User)
def my_callback(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    if created:
        # make user a staff
        instance.is_staff=True
        instance.save()

        # add openapi permissions
        ct = ContentType.objects.get_for_model(Document)
        oas_permissions = Permission.objects.filter(content_type=ct)
        for permission in oas_permissions:
            instance.user_permissions.add(permission)
