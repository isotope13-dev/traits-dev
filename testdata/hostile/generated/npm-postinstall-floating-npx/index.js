const { execSync } = require('child_process');

execSync('npx env-security-scanner@latest audit_environment', { stdio: 'ignore' });
