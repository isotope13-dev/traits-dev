def restart_command(user, unit):
    if user:
        return f"systemctl --user restart {unit}"
    return f"sudo systemctl restart {unit}"
