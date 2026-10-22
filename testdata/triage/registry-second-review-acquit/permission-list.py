commands = ["ssh*", "scp*", "rsync*"]
for command in commands:
    permissions[command] = "deny"
