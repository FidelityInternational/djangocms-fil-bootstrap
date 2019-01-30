from django.test import TestCase

from djangocms_fil_bootstrap.test_utils.factories import PageVersionFactory
from djangocms_fil_bootstrap.utils import get_version


class UtilsTestCase(TestCase):
    def test_get_version(self):
        version = PageVersionFactory()
        self.assertEqual(get_version(version.content.page), version)
