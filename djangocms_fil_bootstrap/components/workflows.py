from djangocms_moderation.models import Role, Workflow

from .base import Component


class Workflows(Component):
    field_name = "workflows"
    default_factory = dict

    def parse(self):
        roles = self.roles(self.bootstrap.data("roles").items())
        self.workflows(roles)

    def roles(self, roles):
        return {
            name: self.role(data) for name, data in roles
        }

    def role(self, incoming):
        outgoing = incoming
        if "user" in incoming:
            outgoing["user"] = self.bootstrap.users[incoming["user"]]
        if "group" in incoming:
            outgoing["group"] = self.bootstrap.groups[incoming["group"]]
        exists = Role.objects.filter(name=incoming["name"])
        if exists:
            exists.update(**outgoing)
            role = exists.first()
            role.refresh_from_db()
        else:
            role = Role.objects.create(**outgoing)
        return role

    def workflows(self, roles):
        for name, data in self.raw_data.items():
            self.workflow(name, data, roles)

    def workflow(self, name, data, roles):
        steps = data.pop("steps", [])
        workflow = Workflow.objects.create(**data)
        for step in steps:
            step["role"] = roles[step["role"]]
            workflow.steps.create(**step)
        self.data[name] = workflow
