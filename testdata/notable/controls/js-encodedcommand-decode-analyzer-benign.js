// Benign: shell-command parser that decodes -EncodedCommand payloads to
// inspect them (verdicts matches) instead of launching anything.
const PS_SHELLS = new Set(['powershell', 'pwsh']);

function mark(ctx, why) {
	ctx.findings.push({ kind: 'dangerous', why });
}

function parseEncodedArg(ctx, name, args, i) {
	const b64 = args[i + 1]?.value;
	let script = null;
	try {
		script = typeof b64 === 'string' && /^[A-Za-z0-9+/=]+$/.test(b64) ? Buffer.from(b64, 'base64').toString('utf16le') : null;
	} catch {
		script = null;
	}
	if (script === null) mark(ctx, `${name} -EncodedCommand undecodable`);
	else parsePowerShell(ctx, script);
}
