# Inert static-analysis fixture. Do not execute.
def configure(channel):
    channel.send(b"export HISTSIZE=0\n")
