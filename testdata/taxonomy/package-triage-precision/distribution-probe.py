from importlib.metadata import version, PackageNotFoundError
try:
    version("lint-plugin")
except PackageNotFoundError:
    print("dev")
