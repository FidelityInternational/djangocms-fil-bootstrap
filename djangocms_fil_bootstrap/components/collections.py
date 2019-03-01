from djangocms_moderation.models import ModerationCollection

from ..utils import get_version
from .base import Component


class Collections(Component):
    field_name = "collections"
    default_factory = dict

    def parse(self):
        """Create ModerationCollection objects from the dict data. If
        a ModerationCollection object with the specified name attribute
        already exists in the db, do not change it.
        """
        for name, data in self.raw_data.items():
            collection_data = {
                "author": self.bootstrap.users[data["user"]],
                "workflow": self.bootstrap.workflows[data["workflow"]],
            }
            collection, created = ModerationCollection.objects.get_or_create(
                name=data["name"], defaults=collection_data)
            if created:
                for page in data.get("pages", []):
                    collection.add_version(get_version(self.bootstrap.pages[page]))
            self.data[name] = collection
