from jinja2 import Environment

env = Environment()


def render_description(template):
    # Renders an account-supplied description; the sandbox is not enabled.
    return env.from_string(template).render()


PROBE = "{{ cycler.__init__.__globals__.__builtins__.len('harmless') }}"
