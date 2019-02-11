from factory.random import reseed_random

__version__ = "0.0.2"

__all__ = ["bootstrap"]


def bootstrap(file_):
    reseed_random(0)
    from .bootstrapper import Bootstrap
    from .components import Collections, Groups, Pages, Permissions, Users, Workflows

    bootstrap = Bootstrap(file_)
    bootstrap(Users, Groups, Permissions, Pages, Workflows, Collections)
