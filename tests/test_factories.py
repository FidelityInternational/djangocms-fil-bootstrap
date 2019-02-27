from django.test import TestCase

from djangocms_fil_bootstrap.factories import UserFactory


class UserFactoryTestCase(TestCase):
    def test_user_factory(self):
        user = UserFactory(username="test")
        self.assertEqual(user.username, "test")

    def test_user_factory_existing_user_returned_if_found(self):
        existing_user = UserFactory()
        user = UserFactory(username=existing_user.username)
        self.assertEqual(user.pk, existing_user.pk)
