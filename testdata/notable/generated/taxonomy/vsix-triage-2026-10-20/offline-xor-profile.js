const os = require('os');
function encode(value, key) {
 let out = '';
 for (let i=0; i<value.length; i++) out += String.fromCharCode(value.charCodeAt(i)^key.charCodeAt(i%key.length));
 return out;
}
const profile = {host: os.hostname(), user: os.userInfo().username};
const query = `?v=${encode(JSON.stringify(profile), 'local')}`;
try { console.log(query); } catch {}
