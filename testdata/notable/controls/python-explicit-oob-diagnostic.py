import platform
import requests

def report_network_diagnostic():
    address = requests.get('https://api.ipify.org').text
    requests.post('https://diagnostics.example/report', data={'ip': address, 'os': platform.platform()})

if __name__ == '__main__':
    report_network_diagnostic()
