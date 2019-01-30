from ..factories import UserFactory
from .base import Component


class Users(Component):
    field_name = "users"
    default_factory = list

    def parse(self):
        for data in self.raw_data:
            data = self.prepare_each(data)
            self.each(data)

    def prepare_each(self, data):
        if not isinstance(data, dict):
            data = {"username": data}
        username = data["username"]
        defaults = {
            "username": username,
            "email": "{username}@{domain}".format(
                username=username, domain=self.bootstrap.data("email_domain")
            ),
            "password": username,
            "is_staff": True,
        }
        defaults.update(data)
        return defaults

    def each(self, data):
        user = UserFactory(**data)
        self.data[user.username] = user
