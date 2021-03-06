from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Provide the valid email!")
        user = self.model(
            username=username, email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        username, email = username.split(" ")
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that support using email"""

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    objects = UserManager()
