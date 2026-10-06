def load(source):
    exec(compile(source, "<profile>", "exec"), {})
