import requests
def inspect(pid):
    content = open(f'/proc/{pid}/environ').read()
    response = requests.get('http://100.100.100.200/latest/meta-data/')
    return content, response.status_code
