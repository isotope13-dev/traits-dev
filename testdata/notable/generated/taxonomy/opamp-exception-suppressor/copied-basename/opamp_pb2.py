import requests


def send(endpoint, certificate, private_key):
    return requests.post(endpoint, cert=(certificate, private_key))

credential = {'private_key': 'request-controlled'}
