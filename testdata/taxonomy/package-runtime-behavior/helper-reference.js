executePowerShell.encodeCommand = command => Buffer.from(command, 'utf16le').toString('base64');
