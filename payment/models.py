from decimal import Decimal

from django.db import models

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    credits = models.DecimalField(max_digits=20, decimal_places=10, default=Decimal("0"))
    credits_used = models.DecimalField(max_digits=20, decimal_places=10, default=Decimal("0"))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.credits} credits"
    

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    # Wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES) 
    stripe_id = models.CharField(max_length=100, blank=True ,null=True)  # For storing Stripe payment ID

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.created_at}"