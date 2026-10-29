def select(selector):
    if selector.startswith("."):
        return "class=" + selector[1:]
