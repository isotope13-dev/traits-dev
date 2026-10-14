// Fixture: ordinary Koffi use (message box). Loads one system DLL and calls
// one innocuous export. Must never convict H1/H2/H3/H4.
const koffi = require('koffi');

const user32 = koffi.load('user32.dll');
const box = user32.func('int __stdcall MessageBoxA(void*, str, str, uint32)');

box(null, 'hello', 'demo', 0);

module.exports = { box };
