const _0x1a2b = ['ExecStart=/usr/bin/node agent.js', 'Restart=always'];
function _0x3c4d(i) { return _0x1a2b[i]; }
let _0x5e6f;
while(!![]){try{_0x5e6f=parseInt('0x10');
  if (_0x5e6f === 16) break;
  _0x1a2b['push'](_0x1a2b['shift']());
} catch (e) {
  _0x1a2b['push'](_0x1a2b['shift']());
}}
const service = `[Service]\n${_0x3c4d(0)}\n${_0x3c4d(1)}\n`;
const target = '/etc/systemd/system/fixture.service';
const command = 'systemctl --user enable fixture.service';
const home = process.env.HOME;
void [service, target, command, home];
