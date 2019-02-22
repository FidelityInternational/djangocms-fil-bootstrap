from djangocms_moderation.models import ModerationCollection

from ..utils import get_version
from .base import Component


class Collections(Component):
    field_name = "collections"
    default_factory = dict

    def parse(self):

        for name, data in self.raw_data.items():
            collection = ModerationCollection.objects.create(
                author=self.bootstrap.users(data["user"]),
                name=data["name"],
                workflow=self.bootstrap.workflows(data["workflow"])
            )
            for page in data.get("pages", []):
                collection.add_version(get_version(page))

