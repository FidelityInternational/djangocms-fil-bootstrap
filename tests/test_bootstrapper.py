from unittest.mock import Mock, call, mock_open, patch

from django.test import TestCase

from djangocms_fil_bootstrap.bootstrapper import Bootstrap


class BootstrapTestCase(TestCase):
    def test_init(self):
        file_ = Mock()
        with patch.object(Bootstrap, "load") as load:
            Bootstrap(file_)
        load.assert_called_once_with(file_)

    def test_from_file(self):
        filename = "foo"
        with patch.object(Bootstrap, "load") as load, patch(
            "builtins.open", mock_open()
        ) as file:
            Bootstrap.from_file(filename)
        file.assert_called_once_with(filename)
        load.assert_called_once_with(file.return_value)

    def test_load(self):
        file_ = Mock()
        with patch("json.load") as json_load:
            bootstrap = Bootstrap(file_)
        json_load.assert_called_once_with(file_)
        self.assertEqual(bootstrap.raw_data, json_load.return_value)

    def test_data(self):
        with patch.object(Bootstrap, "load"):
            bootstrap = Bootstrap(Mock())
            bootstrap.raw_data = {"test": "bar"}

        self.assertEqual(bootstrap.data("test"), "bar")

    def test_call(self):
        with patch.object(Bootstrap, "load"):
            bootstrap = Bootstrap(Mock())
        with patch.object(bootstrap, "each") as each:
            bootstrap(1, 2, 3)
        each.assert_has_calls([call(1), call(2), call(3)])

    def test_each(self):
        with patch.object(Bootstrap, "load"):
            bootstrap = Bootstrap(Mock())

        component_class = Mock(
            spec=[], return_value=Mock(spec=[], field_name="test_field")
        )
        component = component_class.return_value
        with patch.object(bootstrap, "data") as data:
            bootstrap.each(component_class)
        self.assertEqual(bootstrap.test_field, component)
        data.assert_called_once_with("test_field")
        component.assert_called_once_with(data.return_value)
