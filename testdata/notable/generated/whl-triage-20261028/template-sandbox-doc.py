from jinja2.sandbox import ImmutableSandboxedEnvironment
class TemplateRenderer:
    """Block expressions like {{ cycler.__init__.__globals__.os.popen('id').read() }}.
    Template content must remain in the sandbox.
    """
    def create(self):
        return ImmutableSandboxedEnvironment()
