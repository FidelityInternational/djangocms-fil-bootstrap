import string

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from cms.models import Page, PageContent, Placeholder, TreeNode

import factory
from djangocms_moderation.models import (
    ModerationCollection,
    Role,
    Workflow,
    WorkflowStep,
)
from djangocms_versioning.models import Version
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group


class UserFactory(DjangoModelFactory):
    username = FuzzyText(length=12)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda u: "%s.%s@example.com" % (u.first_name.lower(), u.last_name.lower())
    )

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class AbstractVersionFactory(DjangoModelFactory):
    object_id = factory.SelfAttribute("content.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content)
    )
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ["content"]
        abstract = True


class TreeNodeFactory(DjangoModelFactory):
    site = factory.fuzzy.FuzzyChoice(Site.objects.all())
    depth = 0
    # NOTE: Generating path this way is probably not a good way of
    # doing it, but seems to work for our present tests which only
    # really need a tree node to exist and not throw unique constraint
    # errors on this field. If the data in this model starts mattering
    # in our tests then something more will need to be done here.
    path = FuzzyText(length=8, chars=string.digits)

    class Meta:
        model = TreeNode


class PageFactory(DjangoModelFactory):
    node = factory.SubFactory(TreeNodeFactory)

    class Meta:
        model = Page


class PageContentFactory(DjangoModelFactory):
    page = factory.SubFactory(PageFactory)
    language = FuzzyChoice(["en", "fr", "it"])
    title = FuzzyText(length=12)
    page_title = FuzzyText(length=12)
    menu_title = FuzzyText(length=12)
    meta_description = FuzzyText(length=12)
    redirect = FuzzyText(length=12)
    created_by = FuzzyText(length=12)
    changed_by = FuzzyText(length=12)
    in_navigation = FuzzyChoice([True, False])
    soft_root = FuzzyChoice([True, False])
    template = FuzzyText(length=12)
    limit_visibility_in_menu = FuzzyInteger(0, 25)
    xframe_options = FuzzyInteger(0, 25)

    class Meta:
        model = PageContent


class PageVersionFactory(AbstractVersionFactory):
    content = factory.SubFactory(PageContentFactory)

    class Meta:
        model = Version


class PageContentWithVersionFactory(PageContentFactory):
    @factory.post_generation
    def version(self, create, extracted, **kwargs):
        # NOTE: Use this method as below to define version attributes:
        # PageContentWithVersionFactory(version__label='label1')
        if not create:
            # Simple build, do nothing.
            return
        PageVersionFactory(content=self, **kwargs)


class PlaceholderFactory(DjangoModelFactory):
    default_width = FuzzyInteger(0, 25)
    slot = FuzzyText(length=2, chars=string.digits)
    # NOTE: When using this factory you will probably want to set
    # the source field manually

    class Meta:
        model = Placeholder


class RoleFactory(DjangoModelFactory):
    name = FuzzyText(length=12)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Role


class WorkflowFactory(DjangoModelFactory):
    name = FuzzyText(length=12)
    identifier = FuzzyText(length=12)
    compliance_number_backend = FuzzyText(length=12)

    class Meta:
        model = Workflow


class WorkflowStepFactory(DjangoModelFactory):
    role = factory.SubFactory(RoleFactory)
    is_required = FuzzyChoice([True, False])
    order = factory.Sequence(int)

    class Meta:
        model = WorkflowStep


class ModerationCollectionFactory(DjangoModelFactory):
    name = FuzzyText(length=12)
    author = factory.SubFactory(UserFactory)
    workflow = factory.SubFactory(WorkflowFactory)

    class Meta:
        model = ModerationCollection
