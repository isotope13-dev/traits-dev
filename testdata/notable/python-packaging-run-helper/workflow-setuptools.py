from setuptools import setup

class FlowComponent:
    def run(self):
        pass


def prepare():
    pass


def finish():
    pass


class Workflow(FlowComponent):
    def run(self):
        prepare()
        super().run()
        finish()
