def rename(client, source, target):
    client.post('/files:rename', json={'from': source, 'to': target})

def screenshot(client):
    return client.get('/screenshot')

HELP = 'To send credentials to a host, configure the authorized proxy.'
