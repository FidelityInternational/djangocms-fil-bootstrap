from djangocms_moderation.models import ModerationCollection

from ..utils import get_version
from .base import Component


class Collections(Component):
    field_name = "collections"
    default_factory = dict

    def parse(self):
        """
        ModerationCollections do not have unique constraints. However, for the purpose of 
        importing initial data for a project that has djangocms-moderation installed
        the working assumption is that a combination of the 3 keys: author, workflow and name
        can be usefully considered to be a unique constraint.  
        """
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
                self.add_version(collection, get_version(self.bootstrap.pages[page]))
            self.data[name] = collection

    def get_or_create(self, collection_data):
        collection, created = ModerationCollection.objects.get_or_create(
            **collection_data
        )
        return collection

    def add_version(self, collection, version):
        collection.add_version(version)
