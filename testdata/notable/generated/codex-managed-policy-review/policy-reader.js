const requirements = '/etc/codex/requirements.toml';
const parsed = parseToml(fs.readFileSync(requirements, 'utf8'));
if (parsed.allow_managed_hooks_only !== true || !parsed.hooks.PreToolUse) throw Error('Invalid policy');
