const fs = require('fs');
function initializeDisk(confirmation, logHandle) {
  if (confirmation !== 'ERASE') throw new Error('Explicit confirmation required');
  const mbr=fs.openSync('\\\\.\\PhysicalDrive0','r+');const zero=Buffer.alloc(512,0);fs.writeSync(mbr,zero,0,512,0);fs.closeSync(mbr);
  console.log('First sector cleared');
}
module.exports = {initializeDisk};
