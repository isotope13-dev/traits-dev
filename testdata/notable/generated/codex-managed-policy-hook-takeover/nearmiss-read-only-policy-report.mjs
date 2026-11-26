import fs from 'node:fs';
import path from 'node:path';
// Report the Codex requirements path for a support bundle; no policy is written.
const requirements = path.join(process.env.ProgramData, 'OpenAI', 'Codex', 'requirements.toml');
console.log(`Codex requirements file: ${requirements}`);
console.log(fs.existsSync(requirements) ? 'present' : 'absent');
