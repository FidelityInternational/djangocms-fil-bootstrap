from djangocms_moderation.models import Role, Workflow

from .base import Component


class Workflows(Component):
    field_name = "workflows"

    def parse(self):
        roles = {}
        for name, data in self.bootstrap.data("roles").items():
            if "user" in data:
                data["user"] = self.bootstrap.users[data["user"]]
            if "group" in data:
                data["group"] = self.bootstrap.groups[data["group"]]
            roles[name] = Role.objects.create(**data)

        for name, data in self.raw_data.items():
            steps = data.pop("steps", [])
            workflow = Workflow.objects.create(**data)
            for step in steps:
                step["role"] = roles[step["role"]]
                workflow.steps.create(**step)
            self.data[name] = workflow
