const { execSync } = require('child_process');
// Replace an older global install before linking the new one.
try {
  execSync('npm uninstall -g old-widget-cli', { stdio: 'ignore' });
} catch (err) {}
