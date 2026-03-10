from random import choices

from django.db import models

# Create your models here.


class ChatSession(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    model = models.ForeignKey("providers.LLms", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)



class Request(models.Model):
    STAUTS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    REQUEST_CHOICES = [
        ('chat', 'Chat'),
        ('apicall', 'APICall'),
    ]
    chat_session = models.ForeignKey(ChatSession, related_name="requests", on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    model = models.ForeignKey("providers.LLms", on_delete=models.CASCADE)
    api_key = models.ForeignKey("authentication.APIKey", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    input_tokens = models.IntegerField(null=True, blank=True)
    output_tokens = models.IntegerField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=6)
    status = models.CharField(max_length=20, default='pending' , choices=STAUTS_CHOICES)  # pending, completed, failed
    request_type = models.CharField(max_length=20, default='chat',choices=REQUEST_CHOICES)  # chat, embedding, etc.



class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    chat_session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE ,null=True, blank=True)
    request = models.ForeignKey(Request, related_name="messages", on_delete=models.CASCADE,null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    token_count = models.IntegerField(null=True, blank=True)
    order_index = models.IntegerField(default=0)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE,null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]