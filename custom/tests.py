from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CustomUser, UserActivationToken
from .serilaziers import UserSerializer


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(not admin_user.is_confirmed)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)

    def test_save_delete_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        user.save()
        self.assertEqual(User.objects.get(email='normal@user.com'), user)
        user.delete()
        self.assertEqual(User.objects.filter(email='normal@user.com').first(), None)


class UsersAPITests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = APIClient()

    def create_user(self, email, password):
        payload = {'email': email, 'password': password}
        url = reverse("user-api:user-list")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def get_authorization_token(self, email, password):
        url = reverse("user-api:user-login")
        payload = {"username": email, "password": password}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["token"]

    def test_user_serializer(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        serialized_user = UserSerializer(user)
        self.assertEqual(serialized_user.data["email"], 'normal@user.com')
        deserialized_user = UserSerializer(serialized_user)

    def test_api_user_creation(self):
        response = self.create_user(email='normal@user.com', password="foo")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserActivationToken.objects.get(user__email='normal@user.com'))

    def test_api_user_list(self):
        url = reverse("user-api:user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.create_user(email='normal1@user.com', password="foo")
        self.create_user(email='normal2@user.com', password="foo")
        token = self.get_authorization_token("normal1@user.com", "foo")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_password_change(self):
        self.create_user(email='normal1@user.com', password="foo")
        token = self.get_authorization_token("normal1@user.com", "foo")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        id = CustomUser.objects.get(email='normal1@user.com').id
        url = reverse("user-api:password-change", kwargs={"uid": id})
        payload = {"old_password": "foo", "new_password": "boooooooooo"}
        response = client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_activate_user(self):
        self.create_user(email='normal1@user.com', password="foo")
        self.assertEqual(len(mail.outbox), 1)
        token = mail.outbox[0].body.split("token=")[1]
        url = reverse("user-api:user-activate-confirm")
        payload = {"token": token}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CustomUser.objects.get(email='normal1@user.com').is_confirmed)

    def test_reset_password(self):
        self.create_user(email='normal1@user.com', password="foo")
        url = reverse("user-api:password-reset")
        payload = {"email": 'normal1@user.com'}
        self.client.post(url, payload, format="json")
        token = mail.outbox[1].body.split("token=")[1]
        url = reverse("user-api:password-reset-confirm")
        payload = {"token": token, "password": "bungaloooooo"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
