import json
with open("/home/user/.docker/config.json") as stream:
    config = json.load(stream)
defaults = {"auths": {}}
print(config)
