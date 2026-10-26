class OptionSpec:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


# The unchanged Schemathesis --auth option text is help, not a credential.
AUTH = OptionSpec(
    "--auth",
    "-a",
    help="Authenticate all API requests with basic authentication",
    metavar="USER:PASS",
    type=str,
)
