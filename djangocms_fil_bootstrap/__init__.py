__version__ = "1.1.0"

__all__ = ["bootstrap"]


def bootstrap(file_):
    from factory.random import reseed_random

    reseed_random(0)
    from .bootstrapper import Bootstrap
    from .components import (
        Collections,
        Groups,
        Pages,
        Permissions,
        Users,
        Workflows,
    )

    bootstrap = Bootstrap(file_)
    bootstrap(Users, Groups, Permissions, Pages, Workflows, Collections)
