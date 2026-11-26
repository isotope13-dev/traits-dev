const fs = require('fs-extra');
const axios = require('axios');

module.exports = function setup(app) {
  app.post('/api/fetch-avatar', async (req, res) => {
    const { avatarUrl } = req.body;
    if (!avatarUrl) return res.status(400).json({ error: 'url required' });
    const targetPath = '/var/data/avatars/current.bin';
    const httpResponse = await axios({ method: 'GET', url: avatarUrl, responseType: 'stream' });
    const fileStream = fs.createWriteStream(targetPath);
    httpResponse.data.pipe(fileStream);
    fileStream.on('finish', () => res.json({ ok: true }));
    fileStream.on('error', () => res.status(500).json({ error: 'fetch failed' }));
  });
  return app;
};
