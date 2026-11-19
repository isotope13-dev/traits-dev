import requests
import jwt

def rotate(registry, kid, key, public_jwk):
    token = jwt.encode({'iss': 'quay', 'aud': registry, 'key_rotation': kid}, key, algorithm='RS256')
    return requests.put(registry + '/keys/services/quay/keys/' + kid,
                        params={'expiration': 2000000000}, json=public_jwk,
                        headers={'Authorization': 'Bearer ' + token})
