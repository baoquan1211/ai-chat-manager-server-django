from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
    BasePermission,
)
from .models import User, Department, Role
from .serializers import UserSerializer, DepartmentSerializer, RoleSerializer


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        return bool(
            view.kwargs.get("pk") == request.user.id and request.user.is_authenticated
        )


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsSelf | IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        serializer_class = UserSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        # USER: kieu object
        # print(user)
        # print(request.user)
        serializer_class = UserSerializer(user)
        return Response(serializer_class.data)


class DepartmentView(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [IsAdminUser]

    def list(self, request):
        serializer_class = DepartmentSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        department = get_object_or_404(self.queryset, pk=pk)
        serializer_class = DepartmentSerializer(department)
        return Response(serializer_class.data)


class RoleView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [IsAdminUser]

    def list(self, request):
        serializer_class = RoleSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        role = get_object_or_404(self.queryset, pk=pk)
        serializer_class = RoleSerializer(role)
        return Response(serializer_class.data)
