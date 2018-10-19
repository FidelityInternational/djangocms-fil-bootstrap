from djangocms_moderation.models import ModerationCollection

from .base import Component
from ..utils import get_version


class Collections(Component):
    field_name = "collections"

    def parse(self):
        collection1 = ModerationCollection.objects.create(
            author=self.bootstrap.users["test"],
            name="Collection 1",
            workflow=self.bootstrap.workflows["wf1"],
        )
        collection1.add_version(get_version(self.bootstrap.pages["page1"]))
        collection1.add_version(get_version(self.bootstrap.pages["page2"]))

        collection2 = ModerationCollection.objects.create(
            author=self.bootstrap.users["test2"],
            name="Collection 2",
            workflow=self.bootstrap.workflows["wf2"],
        )
        collection2.add_version(get_version(self.bootstrap.pages["page3"]))
        collection2.add_version(get_version(self.bootstrap.pages["page4"]))

        collection3 = ModerationCollection.objects.create(
            author=self.bootstrap.users["moderator"],
            name="Collection for review",
            workflow=self.bootstrap.workflows["wf4"],
        )
        collection3.add_version(get_version(self.bootstrap.pages["page5"]))
