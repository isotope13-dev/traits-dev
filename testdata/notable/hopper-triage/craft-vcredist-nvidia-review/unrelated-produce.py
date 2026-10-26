class Factory:
    def produce(self, specification):
        return dict(specification)

Factory().produce({"name": "part"})
