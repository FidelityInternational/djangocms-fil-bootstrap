class Component:
    field_name = None

    def __init__(self, bootstrap):
        self.bootstrap = bootstrap

    def __call__(self, raw_data):
        self.data = {}
        self.raw_data = raw_data
        self.parse()

    def __getattr__(self, name):
        return self.data[name]

    def __getitem__(self, name):
        return self.data[name]
