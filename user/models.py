from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_departments"


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_roles"


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, username, name, password, **other_fields)

    def create_user(self, email, username, name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=150, blank=True)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(default=timezone.now, editable=False)
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    update_at = models.DateTimeField(auto_now=True, editable=False)
    delete_at = models.DateTimeField(null=True, default=None)

    objects = CustomAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_users"
