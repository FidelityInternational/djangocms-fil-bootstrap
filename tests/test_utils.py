from django.test import TestCase

from djangocms_fil_bootstrap.test_utils.factories import (
    PageVersionFactory,
    PageContentWithVersionFactory,
    UserFactory,
)
from djangocms_fil_bootstrap.utils import get_version
from djangocms_versioning.constants import ARCHIVED


class UtilsTestCase(TestCase):
    def test_get_version(self):
        version = PageVersionFactory()
        self.assertEqual(get_version(version.content.page), version)

    def test_get_version_for_multiple_versions(self):
        user = UserFactory(username="user1")
        page_content = PageContentWithVersionFactory(version__state=ARCHIVED)
        version = PageVersionFactory(content__page=page_content.page)
        latest_version = version.copy(created_by=user)
        self.assertEqual(get_version(page_content.page), latest_version)
