from django.contrib import admin
from providers.models import LLms, Providers

# Register your models here.
admin.site.register(Providers)
admin.site.register(LLms)