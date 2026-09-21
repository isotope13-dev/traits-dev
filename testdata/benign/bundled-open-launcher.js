// Benign rollup-bundled copy of sindresorhus/open (as shipped inside vite's
// dist chunks): opens a URL/file in the user's preferred app. On Windows it
// shells out to `powershell -EncodedCommand` with a base64 UTF-16LE payload
// to survive quoting bugs -- that flag is URL-opening plumbing here, not
// obfuscated execution. The bundler renamed the `path` import (path$8) and
// stripped the docs comment, so source-spelling identity markers miss it.
const localXdgOpenPath = path$8.join(__dirname, 'xdg-open');

const getWslDrivesMountPoint = (async () => {
	const defaultMountPoint = '/mnt/';
	return defaultMountPoint;
});

const baseOpen = async options => {
	let command;
	const cliArguments = [];
	if (platform === 'win32') {
		command = `${process.env.SYSTEMROOT}\\System32\\WindowsPowerShell\\v1.0\\powershell`;
		cliArguments.push(
			'-NoProfile',
			'-NonInteractive',
			'–ExecutionPolicy',
			'Bypass',
			'-EncodedCommand'
		);

		const encodedArguments = ['Start'];
		if (options.target) {
			encodedArguments.push(`"${options.target}"`);
		}

		// Using Base64-encoded command, accepted by PowerShell, to allow special characters.
		options.target = Buffer.from(encodedArguments.join(' '), 'utf16le').toString('base64');
	}

	if (options.target) {
		cliArguments.push(options.target);
	}
};
