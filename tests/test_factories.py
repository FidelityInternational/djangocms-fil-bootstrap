from django.test import TestCase

from djangocms_fil_bootstrap.factories import UserFactory


class UserFactoryTestCase(TestCase):
    def test_user_factory(self):
        user = UserFactory(username="test")
        self.assertEqual(user.username, "test")
