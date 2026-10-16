# Direct configuration access, one-level project navigation, and different
# filenames do not establish the targeted multi-level traversal.
paths = [
    "appsettings.Production.json",
    "../web.config",
    "../../application.json",
    "../../web.config.backup",
]
print(paths)
