// Benign: sindresorhus/open Windows URL-opener plumbing (v7 shape).
const wslToWindowsPath = async path => path;
const encodedArguments = ['Start'];
const target = Buffer.from(encodedArguments.join(' '), 'utf16le').toString('base64');
const path = require('node:path');
const localXdgOpenPath = path.join(__dirname, 'xdg-open');
async function launch(target) {
	const { default: x } = await import('node:child_process');
	x.spawn('powershell', ['-NoProfile', '-NonInteractive', '-EncodedCommand', target]);
}
