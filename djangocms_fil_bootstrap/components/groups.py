from django.contrib.auth.models import Group

from .base import Component


class Groups(Component):
    field_name = "groups"

    def parse(self):
        for name, data in self.raw_data.items():
            group = Group.objects.create(name=data["name"])
            for username in data["users"]:
                user = self.bootstrap.users[username]
                user.groups.add(group)
            self.data[name] = group
