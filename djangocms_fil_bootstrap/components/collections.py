from djangocms_moderation.models import ModerationCollection

from ..utils import get_version
from .base import Component


class Collections(Component):
    field_name = "collections"
    default_factory = dict

    def parse(self):
        for name, data in self.raw_data.items():
            collection_data = {
                "author": self.bootstrap.users[data["user"]],
                "workflow": self.bootstrap.workflows[data["workflow"]]
            }
            collection = self.get_or_create(collection_data)
            import ipdb; ipdb.set_trace()
            for page in data.get("pages", []):
                self.add_version(collection, get_version(self.bootstrap.pages.data.get(page)))

    def get_or_create(self, collection_data):
        collection, created = ModerationCollection.objects.get_or_create(**collection_data)
        return collection

    def add_version(self, collection, version):
        collection.add_version(version)