import json


class Bootstrap:
    def __init__(self, file):
        self.load(file)

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return Bootstrap(f)

    def __call__(self, *components):
        for component in components:
            self.each(component)

    def each(self, component_class):
        component = component_class(self)
        name = component.field_name
        setattr(self, name, component)
        component(self.data(name))

    def load(self, file):
        self.raw_data = json.load(file)

    def data(self, name):
        return self.raw_data.get(name)
