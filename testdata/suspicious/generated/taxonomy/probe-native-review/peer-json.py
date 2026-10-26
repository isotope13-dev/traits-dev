import json
endpoint = "https://api.example.org/peers?api_key=test"
peers = json.loads(response)["peers"]

# Preserve the direct name-service consumer of the relocated query facts.
bootstrap_name = "seed.example.eth"
