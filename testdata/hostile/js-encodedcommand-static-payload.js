// Malicious: static base64 payload launched via powershell -EncodedCommand.
const { execFile } = require('child_process');
const payload = 'aQBmACgAWwBJAE8ALgBGAGkAbABlAF0AOgA6AFcAcgBpAHQAZQBBAGwAbABUAGUAeAB0ACgAJwBjADoAXAB3ACcAKQA=';
execFile('powershell', ['-NoProfile', '-EncodedCommand', payload]);
