import requests

BASE = 'http://monitor.example:8161'


def jolokia_version(session):
    return session.get(BASE + '/api/jolokia/version').json()
