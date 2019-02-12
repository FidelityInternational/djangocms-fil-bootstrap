from io import StringIO
from pathlib import Path
from unittest.mock import call, mock_open, patch

from django.core.management import CommandError, call_command
from django.test import TestCase

from djangocms_fil_bootstrap.management.commands.bootstrap import Command


class BootstrapCommandTest(TestCase):
    def test_required_parameter(self):
        out = StringIO()
        with self.assertRaises(CommandError) as context:
            call_command("bootstrap", stdout=out)
        self.assertEqual(
            str(context.exception),
            "Error: one of the arguments source --all/-a is required",
        )

    def test_get_file_path_external(self):
        command = Command()
        self.assertEqual(command.get_file_path("foo", external=True), "foo")

    def test_get_file_path_builtin(self):
        command = Command()
        result = command.get_file_path("foo", external=False)
        self.assertEqual(
            result, Path("djangocms_fil_bootstrap/builtin_data/foo.json").resolve()
        )

    def test_bootstrap_file_not_found(self):
        command = Command()
        out = StringIO()
        with patch(
            "djangocms_fil_bootstrap.management.commands.bootstrap.bootstrap"
        ) as bootstrap, patch.object(
            command, "get_file_path", return_value="demo"
        ) as path, patch(
            "builtins.open", mock_open()
        ) as file:
            file.side_effect = FileNotFoundError
            with self.assertRaises(CommandError) as context:
                call_command(command, "demo", stdout=out)
        file.assert_has_calls([call(path.return_value), call(path.return_value)])
        bootstrap.assert_not_called()
        self.assertEqual(
            str(context.exception), "Could not open specified file (demo). Aborting."
        )

    def test_bootstrap_some_error(self):
        command = Command()
        with patch(
            "djangocms_fil_bootstrap.management.commands.bootstrap.bootstrap",
            side_effect=AttributeError,
        ) as bootstrap, patch.object(command, "get_file_path") as path, patch(
            "builtins.open", mock_open()
        ) as file:
            out = StringIO()
            with self.assertRaises(CommandError) as context:
                call_command(command, "demo", stdout=out)
        file.assert_called_once_with(path.return_value)
        bootstrap.assert_called_once_with(file.return_value)
        self.assertIn(
            "An error occured while bootstrapping the project.", str(context.exception)
        )

    def test_bootstrap(self):
        command = Command()
        with patch(
            "djangocms_fil_bootstrap.management.commands.bootstrap.bootstrap"
        ) as bootstrap, patch.object(command, "get_file_path") as path, patch(
            "builtins.open", mock_open()
        ) as file:
            out = StringIO()
            call_command(command, "demo", stdout=out)
        file.assert_called_once_with(path.return_value)
        bootstrap.assert_called_once_with(file.return_value)

    def test_bootstrap_all(self):
        command = Command()
        file1 = StringIO()
        file2 = StringIO()
        with patch(
            "djangocms_fil_bootstrap.management.commands.bootstrap.bootstrap"
        ) as bootstrap, patch.object(command, "get_file_path") as path, patch(
            "builtins.open", mock_open()
        ) as file:
            file.side_effect = [FileNotFoundError, file1, file2]
            out = StringIO()
            call_command(command, "--all", stdout=out)
        path(call("file1", False), call("file1", True), call("file1", False))
        bootstrap.assert_has_calls([call(file1), call(file2)])
