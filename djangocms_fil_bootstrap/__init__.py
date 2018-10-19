import os

__version__ = "0.0.0"


def bootstrap():
    from .bootstrap import Bootstrap
    from .components import Collections, Groups, Pages, Permissions, Users, Workflows

    bootstrap = Bootstrap(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    )
    bootstrap(Users, Groups, Permissions, Pages, Workflows, Collections)
