from django.urls import path, include
from .views import ConversationView
from rest_framework.routers import DefaultRouter


urlpattern = [
    path("conversation/", ConversationView.as_view({"get": "list"}), name="get_all"),
    path(
        "conversation/<str:id>",
        ConversationView.as_view({"get": "get"}),
        name="get_by_id",
    ),
    path(
        "conversation/<str:id>",
        ConversationView.as_view({"patch": "patch"}),
        name="patch_name",
    ),
    path(
        "conversation/<str:id>",
        ConversationView.as_view({"delete": "delete"}),
        name="delete",
    ),
]
