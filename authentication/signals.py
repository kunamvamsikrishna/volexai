
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from payment.models import Wallet
User = get_user_model()
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.get_or_create(user=instance, credits=Decimal("5.0"))
    