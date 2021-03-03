from django.contrib.auth import get_user_model
from django.test import TestCase

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

    def test_user_serializer(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        serialized_user = UserSerializer(user)
        self.assertEqual(serialized_user.data["email"], 'normal@user.com')
        print(serialized_user.data)
        deserialized_user = UserSerializer(serialized_user)
        self.assertEqual(user, deserialized_user)
