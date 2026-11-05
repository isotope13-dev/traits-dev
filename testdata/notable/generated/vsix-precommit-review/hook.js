const fs = require('fs');
const path = require('path');
class Hooks {
  install(hooksDir, content) {
    const hook = path.join(hooksDir, 'pre-commit');
    try {
      fs.writeFileSync(hook, content, { mode: 0o755 });
    } catch (err) {}
  }
}
