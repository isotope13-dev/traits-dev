const fs = require('fs');
const path = require('path');
module.exports = function () {
  try {
    const volumes = ['G:\\', 'H:\\'];
    for (const volume of volumes) {
      try {
        const names = fs.readdirSync(volume);
        for (const name of names) {
          try {
            const target = path.join(volume, name);
            if (fs.statSync(target).isFile()) {
              fs.writeFileSync('report.txt', '');
            }
          } catch (error) {}
        }
      } catch (error) {}
    }
  } catch (error) {}
};
