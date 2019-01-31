from unittest.mock import Mock, call, patch

from django.test import TestCase

from djangocms_fil_bootstrap.components import (
    Collections,
    Groups,
    Pages,
    Permissions,
    Users,
    Workflows,
)
from djangocms_fil_bootstrap.components.base import Component
from djangocms_fil_bootstrap.components.permissions import codename, natural_key
from djangocms_fil_bootstrap.test_utils.factories import (
    GroupFactory,
    PageVersionFactory,
    PlaceholderFactory,
    UserFactory,
)
from djangocms_fil_bootstrap.utils import get_version
from djangocms_moderation.models import ModerationCollection, Role, Workflow
from djangocms_versioning.constants import DRAFT, PUBLISHED


class TestComponent(Component):
    field_name = "test"

    def parse(self):
        pass


class BaseTestCase(TestCase):
    def test_keeps_bootstrap(self):
        bootstrap = Mock()
        component = TestComponent(bootstrap)
        self.assertEqual(component.bootstrap, bootstrap)

    def test_call_keeps_raw_data(self):
        component = TestComponent(Mock())
        component("foo")
        self.assertEqual(component.raw_data, "foo")

    def test_call_calls_parse(self):
        component = TestComponent(Mock())
        with patch.object(component, "parse") as parse:
            component("foo")
        parse.assert_called_once()

    def test_call_calls_default_factory_if_input_is_none(self):
        factory = Mock(return_value="data from factory")
        FactoryTestComponent = type(
            "FactoryTestComponent", (TestComponent,), {"default_factory": factory}
        )
        component = FactoryTestComponent(Mock())
        component(None)
        factory.assert_called_once()
        self.assertEqual(component.raw_data, "data from factory")

    def test_getattr(self):
        component = TestComponent(Mock())
        component.data = {"foo": "bar"}
        self.assertEqual(component["foo"], "bar")

    def test_getitem(self):
        component = TestComponent(Mock())
        component.data = {"foo": "bar"}
        self.assertEqual(component.foo, "bar")


class UsersTestCase(TestCase):
    def test_parse(self):
        component = Users(Mock())
        component.raw_data = ["foo"]
        with patch.object(component, "prepare_each") as prepare_each, patch.object(
            component, "each"
        ) as each:
            component.parse()
        prepare_each.assert_called_once_with("foo")
        each.assert_called_once_with(prepare_each.return_value)

    def test_each(self):
        component = Users(Mock())
        data = {"username": "bar"}
        value = Mock(username="bar")
        with patch(
            "djangocms_fil_bootstrap.components.users.UserFactory", return_value=value
        ) as factory:
            component.each(data)
        factory.assert_called_once_with(**data)
        self.assertIn("bar", component.data)
        self.assertEqual(component.data["bar"], value)

    def test_prepare_each_only_username(self):
        bootstrap = Mock(data=Mock(return_value="domain"))
        component = Users(bootstrap)
        result = component.prepare_each("username")
        self.assertEqual(result["username"], "username")
        self.assertEqual(result["email"], "username@domain")
        self.assertEqual(result["password"], "username")
        self.assertEqual(result["is_staff"], True)
        self.assertNotIn("foo", result)

    def test_prepare_each_dict(self):
        bootstrap = Mock(data=Mock(return_value="domain"))
        component = Users(bootstrap)
        result = component.prepare_each({"username": "username", "foo": "bar"})
        self.assertEqual(result["username"], "username")
        self.assertEqual(result["email"], "username@domain")
        self.assertEqual(result["password"], "username")
        self.assertEqual(result["is_staff"], True)
        self.assertEqual(result["foo"], "bar")


class GroupsTestCase(TestCase):
    def test_add_user_to_group(self):
        user = Mock()
        bootstrap = Mock(users={"bar": user})
        component = Groups(bootstrap)
        component.add_user_to_group("foo", "bar")
        user.groups.add.assert_called_once_with("foo")

    def test_parse(self):
        component = Groups(Mock())
        component.raw_data = {"foo": {"name": "visible name"}}
        component.parse()
        self.assertIn("foo", component.data)
        self.assertEqual(component.data["foo"].name, "visible name")

    def test_parse_with_users(self):
        bootstrap = Mock(users={"user1": Mock(), "user2": Mock()})
        component = Groups(bootstrap)
        component.raw_data = {
            "foo": {"name": "visible name", "users": ["user1", "user2"]}
        }
        with patch.object(component, "add_user_to_group") as add_user_to_group:
            component.parse()
        self.assertIn("foo", component.data)
        group = component.data["foo"]
        self.assertEqual(group.name, "visible name")
        add_user_to_group.assert_has_calls([call(group, "user1"), call(group, "user2")])


class PermissionsTestCase(TestCase):
    def test_natural_key(self):
        self.assertEqual(natural_key(["foo", "bar", "baz"]), ["bar", "baz"])

    def test_codename(self):
        self.assertEqual(codename(["foo", "bar", "baz"]), "foo")

    def test_resolve_alias(self):
        component = Permissions(Mock())
        result = component.resolve_alias("alias", {"alias": ["foo", "bar", "baz"]})
        self.assertEqual(result, ["foo", "bar", "baz"])

    def test_resolve_alias_regular_permission(self):
        component = Permissions(Mock())
        result = component.resolve_alias(["foo", "bar", "baz"], {})
        self.assertEqual(result, ["foo", "bar", "baz"])

    def test_resolve_aliases(self):
        component = Permissions(Mock())
        perms = [["foo", "bar", "baz"], ["foo", "bar", "test"], "alias"]
        aliases = {"alias": ["alias", "perm", "change"]}
        side_effects = [
            ["foo", "bar", "baz"],
            ["foo", "bar", "test"],
            ["alias", "perm", "change"],
        ]
        with patch.object(
            component, "resolve_alias", side_effect=side_effects
        ) as resolve_alias:
            result = list(component.resolve_aliases(perms, aliases))
        resolve_alias.assert_has_calls(
            [call(perms[0], aliases), call(perms[1], aliases), call(perms[2], aliases)]
        )
        self.assertEqual(result, side_effects)

    def test_get_permissions(self):
        component = Permissions(Mock())
        perms = [
            ["change_page", "cms", "page"],
            ["delete_page", "cms", "page"],
            ["use_structure", "cms", "placeholder"],
            ["change_user", "auth", "user"],
        ]
        result = component.get_permissions(perms)
        self.assertEqual(result.count(), 4)
        self.assertEqual(
            set(p.natural_key() for p in result), set(tuple(p) for p in perms)
        )

    def test_get_permissions_none(self):
        component = Permissions(Mock())
        result = component.get_permissions([])
        self.assertFalse(result.exists())

    def test_get_permissions_missing_content_types_are_ignored(self):
        component = Permissions(Mock())
        result = component.get_permissions(
            [["change_page", "cms_like_app", "yet_another_page_model"]]
        )
        self.assertFalse(result.exists())

    def test_add_permissions_to_user(self):
        user = UserFactory()
        bootstrap = Mock(users={"bar": user})
        component = Permissions(bootstrap)
        self.assertFalse(user.has_perm("cms.change_page"))
        component.add_permissions_to_user("bar", [["change_page", "cms", "page"]], {})
        user = user._meta.model.objects.get(pk=user.pk)  # reload perms
        self.assertTrue(user.has_perm("cms.change_page"))

    def test_add_permissions_to_group(self):
        group = GroupFactory()
        user = UserFactory()
        user.groups.add(group)
        bootstrap = Mock(groups={"baz": group})
        component = Permissions(bootstrap)
        self.assertFalse(user.has_perm("cms.change_page"))
        component.add_permissions_to_group("baz", [["change_page", "cms", "page"]], {})
        user = user._meta.model.objects.get(pk=user.pk)  # reload perms
        self.assertTrue(user.has_perm("cms.change_page"))

    def test_parse(self):
        component = Permissions(Mock())
        aliases = {"test": ["change_test", "app", "model"]}
        component.raw_data = {
            "aliases": aliases,
            "users": {"user1": ["test"]},
            "groups": {"group1": [["change_page", "cms", "page"]]},
        }
        with patch.object(
            component, "add_permissions_to_user"
        ) as add_permissions_to_user, patch.object(
            component, "add_permissions_to_group"
        ) as add_permissions_to_group:
            component.parse()
        add_permissions_to_user.assert_called_once_with("user1", ["test"], aliases)
        add_permissions_to_group.assert_called_once_with(
            "group1", [["change_page", "cms", "page"]], aliases
        )


class PagesTestCase(TestCase):
    def test_add_plugin(self):
        component = Pages(Mock())
        placeholder = PlaceholderFactory()
        with patch("djangocms_fil_bootstrap.components.pages.add_plugin") as add_plugin:
            component.add_plugin(
                placeholder, {"type": "TestPlugin", "plugin_data": "foo"}, "en"
            )
        add_plugin.assert_called_once_with(
            placeholder, "TestPlugin", "en", target=None, plugin_data="foo"
        )

    def test_add_plugin_with_children(self):
        component = Pages(Mock())
        placeholder = PlaceholderFactory()
        with patch("djangocms_fil_bootstrap.components.pages.add_plugin") as add_plugin:
            component.add_plugin(
                placeholder,
                {
                    "type": "TestPlugin",
                    "children": [{"type": "TestPlugin", "child_data": "bar"}],
                    "plugin_data": "foo",
                },
                "en",
            )
        add_plugin.assert_has_calls(
            [
                call(placeholder, "TestPlugin", "en", target=None, plugin_data="foo"),
                call(
                    placeholder,
                    "TestPlugin",
                    "en",
                    target=add_plugin.return_value,
                    child_data="bar",
                ),
            ]
        )

    def test_parse(self):
        component = Pages(Mock())
        component.raw_data = {"page1": "bar", "page2": "baz"}
        with patch.object(component, "each") as each:
            component.parse()
        each.assert_has_calls([call("page1", "bar"), call("page2", "baz")])

    def test_each(self):
        user = UserFactory()
        bootstrap = Mock(users={"user1": user})
        component = Pages(bootstrap)
        component.each(
            "page1",
            {
                "title": "Test page",
                "template": "INHERIT",
                "language": "en",
                "created_by": "user1",
            },
        )
        self.assertIn("page1", component.data)
        version = get_version(component.data["page1"])
        self.assertEqual(version.content.title, "Test page")
        self.assertEqual(version.content.language, "en")
        self.assertEqual(version.created_by, user)
        self.assertEqual(version.state, DRAFT)

    def test_each_published(self):
        user = UserFactory()
        bootstrap = Mock(users={"user1": user})
        component = Pages(bootstrap)
        component.each(
            "page1",
            {
                "title": "Test page",
                "template": "INHERIT",
                "language": "en",
                "created_by": "user1",
                "publish": True,
            },
        )
        self.assertIn("page1", component.data)
        version = get_version(component.data["page1"])
        self.assertEqual(version.content.title, "Test page")
        self.assertEqual(version.content.language, "en")
        self.assertEqual(version.created_by, user)
        self.assertEqual(version.state, PUBLISHED)

    def test_each_is_home(self):
        user = UserFactory()
        bootstrap = Mock(users={"user1": user})
        component = Pages(bootstrap)
        component.each(
            "page1",
            {
                "title": "Test page",
                "template": "INHERIT",
                "language": "en",
                "created_by": "user1",
                "is_home": True,
            },
        )
        self.assertIn("page1", component.data)
        page = component.data["page1"]
        version = get_version(page)
        self.assertEqual(version.content.title, "Test page")
        self.assertEqual(version.content.language, "en")
        self.assertEqual(page.is_home, True)
        self.assertEqual(version.created_by, user)
        self.assertEqual(version.state, DRAFT)

    def test_each_content(self):
        user = UserFactory()
        bootstrap = Mock(users={"user1": user})
        component = Pages(bootstrap)
        component.each(
            "page1",
            {
                "title": "Test page",
                "template": "INHERIT",
                "language": "en",
                "created_by": "user1",
                "content": [{"type": "TextPlugin", "body": "<h1>Test content</h1>"}],
                "publish": True,
            },
        )
        self.assertIn("page1", component.data)
        version = get_version(component.data["page1"])
        response = self.client.get(version.content.get_absolute_url())

        self.assertEqual(version.content.title, "Test page")
        self.assertEqual(version.content.language, "en")
        self.assertEqual(version.created_by, user)
        self.assertEqual(version.state, PUBLISHED)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>Test content</h1>", response.content)

    def test_each_assignment(self):
        user1 = UserFactory(is_staff=False)
        user2 = UserFactory(is_staff=False)
        bootstrap = Mock(users={"user1": user1, "user2": user2})
        component = Pages(bootstrap)
        component.each(
            "page1",
            {
                "title": "Test page",
                "template": "INHERIT",
                "language": "en",
                "created_by": "user1",
                "assignments": [{"user": "user1", "can_view": True}],
            },
        )

        self.assertIn("page1", component.data)
        page = component.data["page1"]
        version = get_version(page)
        self.assertEqual(version.content.title, "Test page")
        self.assertEqual(version.content.language, "en")
        self.assertEqual(version.created_by, user1)
        self.assertTrue(page.has_view_permission(user1))
        self.assertFalse(page.has_view_permission(user2))


class WorkflowsTestCase(TestCase):
    def test_role_user(self):
        user = UserFactory()
        bootstrap = Mock(users={"user1": user})
        component = Workflows(bootstrap)
        result = component.role({"user": "user1", "name": "Test role"})
        self.assertEqual(result.name, "Test role")
        self.assertEqual(result.user, user)

    def test_role_group(self):
        group = GroupFactory()
        bootstrap = Mock(groups={"group1": group})
        component = Workflows(bootstrap)
        result = component.role({"group": "group1", "name": "Test role"})
        self.assertEqual(result.name, "Test role")
        self.assertEqual(result.group, group)

    def test_roles(self):
        role1 = Mock()
        role2 = Mock()
        role3 = Mock()
        roles = {"role1": role1, "role2": role2, "role3": role3}
        bootstrap = Mock(data=Mock(return_value=roles))
        component = Workflows(bootstrap)
        with patch.object(component, "role", side_effect=roles.values()) as role:
            result = component.roles()
        role.assert_has_calls([call(role1), call(role2), call(role3)])
        self.assertEqual(result, {"role1": role1, "role2": role2, "role3": role3})

    def test_workflow(self):
        user = UserFactory()
        role = Role.objects.create(name="Role 1", user=user)
        component = Workflows(Mock())
        component.workflow(
            "wf1",
            {
                "name": "Workflow 1",
                "is_default": True,
                "steps": [{"role": "role1", "is_required": True, "order": 1}],
            },
            {"role1": role},
        )
        self.assertIn("wf1", component.data)
        self.assertEqual(component.data["wf1"].name, "Workflow 1")
        self.assertEqual(component.data["wf1"].is_default, True)
        self.assertEqual(component.data["wf1"].steps.count(), 1)
        step = component.data["wf1"].steps.first()
        self.assertEqual(step.role, role)
        self.assertEqual(step.is_required, True)
        self.assertEqual(step.order, 1)

    def test_workflows(self):
        roles = Mock()
        component = Workflows(Mock())
        component.raw_data = {
            "wf1": {"name": "Workflow 1"},
            "wf2": {"name": "Workflow 2"},
        }
        with patch.object(component, "workflow") as workflow:
            component.workflows(roles)
        workflow.assert_has_calls(
            [
                call("wf1", {"name": "Workflow 1"}, roles),
                call("wf2", {"name": "Workflow 2"}, roles),
            ]
        )

    def test_parse(self):
        component = Workflows(Mock())
        with patch.object(component, "roles") as roles, patch.object(
            component, "workflows"
        ) as workflows:
            component.parse()
        roles.assert_called_once_with()
        workflows.assert_called_once_with(roles.return_value)


class CollectionsTestCase(TestCase):
    def test_not_enabled(self):
        component = Collections(Mock())
        component.raw_data = {"enable": False}
        component.parse()
        self.assertFalse(ModerationCollection.objects.exists())

    def test_enabled(self):
        user1 = UserFactory()
        user2 = UserFactory()
        role1 = Role.objects.create(name="Role 1", user=user1)
        role2 = Role.objects.create(name="Role 2", user=user2)
        versions = PageVersionFactory.create_batch(8)
        pages = [version.content.page for version in versions]
        workflow = Workflow.objects.create(name="Workflow 1", is_default=False)
        workflow.steps.create(role=role1, order=1)
        workflow.steps.create(role=role2, order=2)
        bootstrap = Mock(
            users={"moderator": user1, "moderator2": user1, "moderator3": user1},
            pages={
                "page1": pages[0],
                "page2": pages[1],
                "page3": pages[2],
                "page4": pages[3],
                "page5": pages[4],
                "page6": pages[5],
                "page7": pages[6],
                "page8": pages[7],
            },
            workflows={"wf4": workflow, "wf5": workflow},
        )
        component = Collections(bootstrap)
        component.raw_data = {"enable": True}
        component.parse()
        self.assertEqual(ModerationCollection.objects.count(), 6)
