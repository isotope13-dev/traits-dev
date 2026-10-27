const fs = require('node:fs');
const {spawn} = require('node:child_process');
async function view(profileUrl, viewer, target) {
  const response = await fetch(profileUrl);
  fs.writeFileSync(target, await response.text());
  spawn(viewer, [target]);
}
view('https://t.me/public_profile', 'viewer.exe', 'profile.html');
