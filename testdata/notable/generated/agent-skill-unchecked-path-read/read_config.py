def read_config(config_name):
    path = f"/etc/app/{config_name}"
    return open(path).read()
