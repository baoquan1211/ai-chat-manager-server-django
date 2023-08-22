from rest_framework import response, status, viewsets
from .models import Conversation
from .serializers import ConversationSerializer


class ConversationView(viewsets.ViewSet):
    """serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()"""

    def list(self, request):
        if request is None:
            return response.Response(
                "Respose is not valid", status=status.HTTP_404_NOT_FOUND
            )
        try:
            conversation_serializer = ConversationSerializer(
                Conversation.objects.all(), many=True
            )

            conversations = conversation_serializer.data
            if conversations:
                return response.Response(conversations, status=status.HTTP_200_OK)
            else:
                return response.Response(
                    "Conversation is not found", status=status.HTTP_404_NOT_FOUND
                )
        except:
            return response.Response(
                "Something went wrong", status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, id):
        if request is None:
            return response.Response(
                "Respose is not valid", status=status.HTTP_404_NOT_FOUND
            )

        try:
            conversation_serializer = ConversationSerializer(
                Conversation.objects.get(id=id)
            )
            print(conversation_serializer)
            conversation = conversation_serializer.data
            return response.Response(conversation, status=status.HTTP_200_OK)
        except:
            return response.Response(
                "Conversation is not found", status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id):
        if request is None:
            return response.Response(
                "Respose is not valid", status=status.HTTP_404_NOT_FOUND
            )
        conversation = ConversationSerializer
        print(request.GET.get("q", ""))
        return response.Response(1)
