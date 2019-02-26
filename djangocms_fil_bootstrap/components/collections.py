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
                "workflow": self.bootstrap.workflows[data["workflow"]],
                "name": data["name"],
            }
            collection = self.get_or_create(collection_data)
            for page in data.get("pages", []):
                # access pages from bootstrap as if a dict because the __getitem__ method in Bootstrap
                # allows this and without it mock objects will fail via other access methods.
                self.add_version(collection, self.get_version(self.bootstrap.pages[page]))
            self.data[name] = collection

    def get_version(self, page):
        return get_version(page)

    def get_or_create(self, collection_data):
        collection, created = ModerationCollection.objects.get_or_create(**collection_data)
        return collection

    def add_version(self, collection, version):
        collection.add_version(version)