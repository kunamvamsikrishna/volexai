from email.policy import default
from pickletools import decimalnl_long
from django.db import models

# Create your models here.


class Providers(models.Model):
    name =  models.CharField(max_length=100)
    is_active = models.BinaryField(default=True)
    url = models.URLField()
    description = models.TextField()
    def __str__(self):
        return self.name


class LLms(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)
    provider = models.ForeignKey(Providers,related_name="llm",on_delete=models.CASCADE)
    input_token_cost = models.DecimalField(max_digits=10,decimal_places=6, default=0)
    output_token_cost = models.DecimalField(max_digits=10,decimal_places=6, default=0)
    context_length = models.IntegerField()
    max_output_tokens = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("name","provider")
    def __str__(self):
        return self.name
