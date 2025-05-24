from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Category

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_balance_category(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(
            name='Saldo',
            description='Kategoria systemowa do śledzenia salda',
            is_system=True,
            is_default=False,
            user=instance
        )