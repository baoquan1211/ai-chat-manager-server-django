from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserView, DepartmentView, RoleView


urlpatterns = [
    path("user/", UserView.as_view({"get": "list"}), name="list-user"),
    path("user/<int:pk>/", UserView.as_view({"get": "retrieve"}), name="detail-user"),
    path(
        "department/", DepartmentView.as_view({"get": "list"}), name="list-department"
    ),
    path(
        "department/<int:pk>/",
        DepartmentView.as_view(
            {"get": "retrieve"},
        ),
        name="detail-department",
    ),
    path("role/", RoleView.as_view({"get": "list"}), name="list-role"),
    path(
        "role/<int:pk>/",
        RoleView.as_view({"get": "retrieve"}),
        name="detail-role",
    ),
]
