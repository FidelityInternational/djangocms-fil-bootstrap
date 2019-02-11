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
    default_factory = dict

    def parse(self):
        aliases = self.raw_data.get("aliases", {})
        for username, perms in self.raw_data.get("users", {}).items():
            self.add_permissions_to_user(username, perms, aliases)
        for group_name, perms in self.raw_data.get("groups", {}).items():
            self.add_permissions_to_group(group_name, perms, aliases)

    def add_permissions_to_user(self, username, perms, aliases):
        user = self.bootstrap.users[username]
        user.user_permissions.add(
            *self.get_permissions(self.resolve_aliases(perms, aliases))
        )

    def add_permissions_to_group(self, group_name, perms, aliases):
        group = self.bootstrap.groups[group_name]
        group.permissions.add(
            *self.get_permissions(self.resolve_aliases(perms, aliases))
        )

    def resolve_aliases(self, perms, aliases):
        for perm in perms:
            yield self.resolve_alias(perm, aliases)

    def resolve_alias(self, perm, aliases):
        if not isinstance(perm, str):
            return perm
        else:
            return aliases[perm]

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
        if not q:
            return Permission.objects.none()
        return Permission.objects.filter(q)
