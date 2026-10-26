def check_policy(lines):
    compile(
        "def policy():\n" + "\n".join("    " + line for line in lines),
        "policy",
        "exec",
    )


def evaluate_lines(lines):
    eval("(" + "\n".join(lines) + ")")


def execute_template(body):
    exec("def wrapper():\n" + body)
