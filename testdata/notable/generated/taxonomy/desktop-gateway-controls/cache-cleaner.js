const fs = require('fs');
const path = require('path');

function clearTempCaches(baseDir) {
  for (const sub of ['Cache', 'Temp', 'GPUCache']) {
    const fullPath = path.join(baseDir, sub);
    if (fs.existsSync(fullPath)) {
      fs.rmSync(fullPath, { recursive: true, force: true });
    }
  }
}

clearTempCaches('profile');
