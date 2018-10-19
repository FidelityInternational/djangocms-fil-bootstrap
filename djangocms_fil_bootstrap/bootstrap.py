import json


class Bootstrap:
    def __init__(self, file):
        self.load(file)

    def __call__(self, *components):
        for Component in components:
            component = Component(self)
            name = component.field_name
            setattr(self, name, component)
            component(self.data(name))

    def load(self, file):
        with open(file) as f:
            self.raw_data = json.load(f)

    def data(self, name):
        return self.raw_data.get(name)
