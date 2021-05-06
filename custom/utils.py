from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.urls import reverse

from .tokens import account_activation_token, password_reset_token


def send_activation_mail(user):
    token = account_activation_token.make_token(user)
    print(token)
    subject = 'Activate your account.'
    domain_url = Site.objects.get_current().domain
    relative_url = reverse("user-api:user-activate-confirm")
    url = "http://" + domain_url + relative_url + "?token=" + token
    message = "Hi, please click this link to acctivate your account: "+url
    email = EmailMessage(
        subject,
        message,
        to=[user.email]
    )
    email.send()


def send_reset_mail(user):
    token = password_reset_token.make_token(user)
    subject = 'Reset your account password.'
    domain_url = Site.objects.get_current().domain
    relative_url = reverse("user-api:password-reset-confirm")
    url = "http://" + domain_url + relative_url + "?token=" + token
    message = "Hi "+user.first_name+", please click this link to reset your account password: "+url
    email = EmailMessage(
        subject,
        message,
        to=[user.email]
    )
    email.send()
