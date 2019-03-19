from djangocms_moderation.models import Role, Workflow

from .base import Component


class Workflows(Component):
    field_name = "workflows"
    default_factory = dict

    def parse(self):
        roles = self.roles()
        self.workflows(roles)

    def roles(self):
        return {
            name: self.role(data) for name, data in self.bootstrap.data("roles").items()
        }

    def role(self, data):
        if "user" in data:
            data["user"] = self.bootstrap.users[data["user"]]
        if "group" in data:
            data["group"] = self.bootstrap.groups[data["group"]]
        role, created = Role.objects.get_or_create(**data)
        return role

    def workflows(self, roles):
        for name, data in self.raw_data.items():
            self.workflow(name, data, roles)

    def workflow(self, name, data, roles):
        steps = data.pop("steps", [])
        workflow_data = {
            "is_default": data["is_default"],
        }
        workflow, created = Workflow.objects.get_or_create(name=data["name"], defaults=workflow_data)
        if created:
            for step in steps:
                step["role"] = roles[step["role"]]
                workflow.steps.create(**step)
            self.data[name] = workflow
