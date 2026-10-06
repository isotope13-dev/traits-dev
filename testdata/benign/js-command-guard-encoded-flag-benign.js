// Benign: command guard that detects encoded-flag spellings and verdicts them.
const PS_ENCODED_FLAG = /^-e(?:c|nc\w*)?$/i;
function classify(cmd, argv) {
	if (/^(?:pwsh|powershell)$/i.test(cmd) && argv.some(a => PS_ENCODED_FLAG.test(a))) {
		return { kind: 'dangerous', why: 'encoded PowerShell command' };
	}
	return { kind: 'ok' };
}
