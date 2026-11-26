"""argv of a shell that records no command history."""


def quiet_shell(route, home):
    data = [
        "TERM=xterm-256color",
        f"HOME={home}",
        "HISTFILE=/dev/null",
        "PS1=# ",
    ]
    return ["/usr/bin/env", "-i", *data, route.bash, "-i"]
