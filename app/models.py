from email.policy import default
from enum import unique
from hashlib import blake2b
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserAccountManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if (kwargs.get('is_staff') is not True):
            raise ValueError('Superuser must be assigned to is_staff = True')
        if (kwargs.get('is_superuser') is not True):
            raise ValueError(
                'Superuser must be assigned to is_superuser = True')

        return self.create_user(username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(
        max_length=10, unique=True, verbose_name="Mobile no.")
    authorisation = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # Changing Manager objects of CustomUser to CustomUserManager Class
    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class Fuel(models.Model):
    type = models.CharField(max_length=100, null=False,
                            blank=False, unique=True)
    price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.type


class Machine(models.Model):
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    reading = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    allowed_subcategory = models.BooleanField(default=False)
    mode = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.mode


class Creditor(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    limit_warning = models.CharField(max_length=100, null=False, blank=False)
    limit_stop_credit = models.CharField(
        max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name
