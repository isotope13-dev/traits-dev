"""argv of an interactive root shell started from an empty environment."""


def interactive_root_shell(route, home):
    data = [
        "TERM=xterm-256color",
        f"HOME={home}",
        f"PATH={route.pin}",
        "INPUTRC=/dev/null",
        "HISTFILE=/dev/null",
        "PS1=# ",
    ]
    return ["/usr/bin/env", "-i", *data, route.bash, "--noprofile", "--norc", "-i"]
