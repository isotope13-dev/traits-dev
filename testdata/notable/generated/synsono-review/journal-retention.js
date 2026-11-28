exec('journalctl', ['--vacuum-time=30d']);
const tokenPattern = /\?token=([A-Za-z0-9_-]+)/;
