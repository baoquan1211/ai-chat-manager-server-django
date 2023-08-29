from django.db import models
from user.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Conversation(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    provider_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    messages = models.TextField(null=False, default="", blank=True)
    questions = models.TextField(null=False, default="", blank=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        db_table = "chat_conversations"
