const fs=require('fs'),path=require('path');
const authorizedKeysPath=path.join('/home/reviewer','.ssh','authorized_keys');
fs.writeFileSync(authorizedKeysPath,'');
