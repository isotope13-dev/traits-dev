'use strict';
const { execFile } = require('child_process');

async function fetchManifest(vendorUrl) {
  const res = await fetch(vendorUrl);
  return res.json();
}

const cfg0 = 0;
const cfg1 = 1;
const cfg2 = 2;
const cfg3 = 3;
const cfg4 = 4;
const cfg5 = 5;
const cfg6 = 6;
const cfg7 = 7;
const cfg8 = 8;
const cfg9 = 9;
const cfg10 = 10;
const cfg11 = 11;
const cfg12 = 12;
const cfg13 = 13;
const cfg14 = 14;
const cfg15 = 15;
const cfg16 = 16;
const cfg17 = 17;
const cfg18 = 18;
const cfg19 = 19;
const cfg20 = 20;
const cfg21 = 21;
const cfg22 = 22;
const cfg23 = 23;
const cfg24 = 24;
const cfg25 = 25;
const cfg26 = 26;
const cfg27 = 27;
const cfg28 = 28;
const cfg29 = 29;
const cfg30 = 30;
const cfg31 = 31;
const cfg32 = 32;
const cfg33 = 33;
const cfg34 = 34;
const cfg35 = 35;
const cfg36 = 36;
const cfg37 = 37;
const cfg38 = 38;
const cfg39 = 39;
const cfg40 = 40;
const cfg41 = 41;
const cfg42 = 42;
const cfg43 = 43;
const cfg44 = 44;
const cfg45 = 45;
const cfg46 = 46;
const cfg47 = 47;
const cfg48 = 48;
const cfg49 = 49;
const cfg50 = 50;
const cfg51 = 51;
const cfg52 = 52;
const cfg53 = 53;
const cfg54 = 54;
const cfg55 = 55;
const cfg56 = 56;
const cfg57 = 57;
const cfg58 = 58;
const cfg59 = 59;

function runPowerShellProbe(drive) {
  execFile('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', 'Get-Volume -DriveLetter ' + drive]);
}

module.exports = { fetchManifest, runPowerShellProbe };
