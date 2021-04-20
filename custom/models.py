from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    CustomUser model where the username,first_name and last_name are removed and the email of the user
    is used for login authentication instead.
    """
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.email)


class UserActivationToken(models.Model):
    user = models.ForeignKey(CustomUser, related_name="activation", on_delete=models.CASCADE)
    activation_token = models.CharField(unique=True, primary_key=True, max_length=400)


class UserResetToken(models.Model):
    user = models.ForeignKey(CustomUser, related_name="reset", on_delete=models.CASCADE)
    reset_token = models.CharField(unique=True, primary_key=True, max_length=400)
