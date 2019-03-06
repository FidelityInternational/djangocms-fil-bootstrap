from django.test import TestCase

from djangocms_versioning.constants import ARCHIVED
from freezegun import freeze_time

from djangocms_fil_bootstrap.test_utils.factories import (
    PageContentWithVersionFactory,
    PageVersionFactory,
)
from djangocms_fil_bootstrap.utils import get_version


class UtilsTestCase(TestCase):
    def test_get_version(self):
        version = PageVersionFactory()
        self.assertEqual(get_version(version.content.page), version)

    def test_get_version_for_multiple_versions(self):
        with freeze_time("2010-10-10"):
            page_content = PageContentWithVersionFactory(version__state=ARCHIVED)
        latest_version = PageVersionFactory(content__page=page_content.page)
        self.assertEqual(get_version(page_content.page), latest_version)
