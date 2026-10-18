# Inert static-analysis fixture. Do not execute.
def configure(channel):
    channel.sendall(b"export HISTSIZE=0 HISTFILESIZE=0\n")
