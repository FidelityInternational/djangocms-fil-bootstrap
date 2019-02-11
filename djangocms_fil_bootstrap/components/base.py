from abc import ABCMeta, abstractmethod


class Component(metaclass=ABCMeta):
    @property
    @abstractmethod
    def field_name(self):
        """Key used to get the data from the data source, as well
        as store the data in bootstrap object.

        Data saved under "foo" key can be used by components
        next in chain by accessing `self.bootstrap.data.foo`.
        """

    """Function that can be defined to create raw_data
    if it doesn't exist in the data source.
    """
    default_factory = None

    def __init__(self, bootstrap):
        self.bootstrap = bootstrap
        self.data = {}
        self.raw_data = None

    def __call__(self, raw_data):
        if raw_data is None and self.default_factory:
            raw_data = self.default_factory()
        self.raw_data = raw_data
        self.parse()

    def __getattr__(self, name):
        return self.data[name]

    def __getitem__(self, name):
        return self.data[name]

    @abstractmethod
    def parse(self):
        """Component logic goes here.

        `self.raw_data` contains data from `self.field_name`
        key in the data source.
        """
