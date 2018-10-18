import logging
from itertools import groupby

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .base import Component


logger = logging.getLogger(__name__)


def natural_key(triple):
    codename, *key = triple
    return key


def codename(triple):
    name, *key = triple
    return name


class Permissions(Component):
    field_name = "permissions"

    def parse(self):
        aliases = self.bootstrap.data("permission_aliases")
        for username, perms in self.raw_data["users"].items():
            user = self.bootstrap.users[username]
            user.user_permissions.add(
                *self.get_permissions(self.resolve_aliases(aliases, perms))
            )
        for group_name, perms in self.raw_data["groups"].items():
            group = self.bootstrap.groups[group_name]
            group.permissions.add(
                *self.get_permissions(self.resolve_aliases(aliases, perms))
            )

    def resolve_aliases(self, aliases, perms):
        for perm in perms:
            if not isinstance(perm, str):
                yield perm
            else:
                yield aliases[perm]

    def get_permissions(self, perms):
        q = Q()
        perms = sorted(perms, key=natural_key)
        for key, group in groupby(perms, natural_key):
            try:
                ctype = ContentType.objects.get_by_natural_key(*key)
            except ContentType.DoesNotExist:
                logger.debug("Missing content type: %(ctype)s", key)
                continue
            q |= Q(content_type=ctype, codename__in=[codename(perm) for perm in group])
        return Permission.objects.filter(q)
