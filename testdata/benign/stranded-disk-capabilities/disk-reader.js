const disk = require('fs');
// A read-only disk tool should retain the neutral disk-open observation.
function readSector() {
  const fd = disk.openSync('\\\\.\\PhysicalDrive7', 'r');
  const sector = Buffer.alloc(512);
  disk.readSync(fd, sector, 0, sector.length, 0);
  disk.closeSync(fd);
  return sector;
}
module.exports = readSector;
