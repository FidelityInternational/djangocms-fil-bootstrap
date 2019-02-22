from django.contrib.auth.models import Group

from .base import Component


class Groups(Component):
    field_name = "groups"
    default_factory = dict

    def parse(self):
        for name, data in self.raw_data.items():
            exists = Group.objects.filter(name=data["name"])
            if exists:
                group = exists.first()
            else: 
                group = Group.objects.create(name=data["name"])
            for username in data.get("users", []):
                self.add_user_to_group(group, username)
            self.data[name] = group

    def add_user_to_group(self, group, username):
        user = self.bootstrap.users[username]
        user.groups.add(group)

