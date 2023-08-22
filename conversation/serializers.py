from rest_framework import serializers
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            "user_id",
            "provider_id",
            "name",
            "messages",
            "questions",
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        return data
