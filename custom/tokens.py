import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int

from .models import UserActivationToken, UserResetToken


class ActivationTokenGenerator(PasswordResetTokenGenerator):

    """
    Create token and save it into the database
    """

    def make_token(self, user):
        token = super().make_token(user)
        user_token = UserActivationToken.objects.update_or_create(
            defaults={"activation_token": token},
            user=user
        )
        return token

    """
    Ensure that the token is valid even if user changes
    """

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

    """
    Remove the expiration time of the token
    """

    def check_token(self, user, token):
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        return True


class ResetTokenGenerator(PasswordResetTokenGenerator):

    """
    Create token and save it into the database
    """

    def make_token(self, user):
        token = super().make_token(user)
        user_token = UserResetToken.objects.update_or_create(
            defaults={"reset_token": token},
            user=user
        )
        return token


account_activation_token = ActivationTokenGenerator()
password_reset_token = ResetTokenGenerator()
