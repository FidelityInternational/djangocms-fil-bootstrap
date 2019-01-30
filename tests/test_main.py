from unittest.mock import Mock, patch

from django.test import TestCase

from djangocms_fil_bootstrap import bootstrap
from djangocms_fil_bootstrap.components import (
    Collections,
    Groups,
    Pages,
    Permissions,
    Users,
    Workflows,
)


class MainTestCase(TestCase):
    def test_bootstrap(self):
        file_ = Mock()
        with patch("djangocms_fil_bootstrap.reseed_random") as reseed_random, patch(
            "djangocms_fil_bootstrap.bootstrapper.Bootstrap"
        ) as Bootstrap:
            bootstrap(file_)
        Bootstrap.assert_called_once_with(file_)
        Bootstrap.return_value.assert_called_once_with(
            Users, Groups, Permissions, Pages, Workflows, Collections
        )
        reseed_random.assert_called_once_with(0)
