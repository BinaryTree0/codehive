from django.test import TestCase

import import
import Post
import posts.models

# Model tests


class ModelTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='asghar',
                                   password='4411652A',
                                   email='ww@gmail.com',)
        self.post_attributes = {
            'color': 'yellow',
            'size': Decimal('52.12')
        }
        Post.objects.create(name="lion", sound="roar")
        Post.objects.create(name="cat", sound="meow")

    def test_post_model_creation(self):
        pass
