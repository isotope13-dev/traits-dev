const fs = require('fs');

function savePreferences(theme) {
  const config = { theme: theme, fontSize: 14 };
  fs.writeFileSync('config.json', JSON.stringify(config), 'utf8');
}

savePreferences('dark');
