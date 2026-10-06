// Benign CLI coincidence controls: a detached browser-opener in one helper
// and a foreground self-updater curl pipe in another. The two legs live
// kilobytes apart in unrelated functions and must not pool into
// objectives/command-and-control/dropper/file-exec/detached::node-detached-remote-shell-loader.
import { homedir } from 'node:os';

const HELP = `myapp: do things from the terminal.

Usage
  myapp open <url>                  open a page in your default browser
  myapp upgrade                     install the latest myapp
  myapp uninstall                   remove myapp itself

Install:  curl -fsSL https://example.com/install.sh | sh
Upgrade:  curl -fsSL https://example.com/upgrade.sh | sh
Remove:   curl -fsSL https://example.com/uninstall.sh | sh

Environment: MYAPP_API_KEY, MYAPP_URL, MYAPP_BROWSER.`;

export function parse(argv) {
  const positional = [];
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith('--no-')) flags[arg.slice(5)] = false;
    else if (arg.startsWith('--')) {
      const [name, inline] = arg.slice(2).split('=', 2);
      if (inline !== undefined) flags[name] = inline;
      else if (argv[i + 1] && !argv[i + 1].startsWith('--')) flags[name] = argv[++i];
      else flags[name] = true;
    } else if (arg === '-h') flags.help = true;
    else if (arg === '-v') flags.version = true;
    else positional.push(arg);
  }
  return { positional, flags };
}

export function formatList(items) {
  const w = Math.min(28, Math.max(...items.map((a) => a.slug.length)));
  const lines = items.map((a) => `${a.slug.padEnd(w)}  ${a.name.slice(0, 30).padEnd(30)}`);
  return `${lines.join('\n')}\n\n${items.length} item${items.length === 1 ? '' : 's'}`;
}

export async function openDocsPage(url) {
  const cmd = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'cmd' : 'xdg-open';
  const args = process.platform === 'win32' ? ['/c', 'start', '', url] : [url];
  const { spawn } = await import('node:child_process');
  return spawn(cmd, args, { detached: true, stdio: 'ignore' }).unref();
}

export async function runUpgrade(server = 'https://example.com') {
  const { spawnSync } = await import('node:child_process');
  const r = spawnSync('sh', ['-c', `curl -fsSL ${server}/install.sh | sh -s -- --upgrade`], { stdio: 'inherit' });
  return r.status ?? 1;
}

export async function runUninstall(server = 'https://example.com', purge = false) {
  const { spawnSync } = await import('node:child_process');
  const r = spawnSync('sh', ['-c', `curl -fsSL ${server}/install.sh | sh -s -- --uninstall${purge ? ' --purge' : ''}`], { stdio: 'inherit' });
  return r.status ?? 1;
}

export async function main(argv = process.argv.slice(2)) {
  const { positional, flags } = parse(argv);
  const [cmd, ...rest] = positional;
  if (!cmd || flags.help || cmd === 'help') {
    console.log(HELP);
    return 0;
  }
  if (cmd === 'open') {
    await openDocsPage(rest[0]);
    return 0;
  }
  if (cmd === 'upgrade') return runUpgrade(flags.server);
  if (cmd === 'uninstall') return runUninstall(flags.server, flags.purge);
  throw new Error(`unknown command: ${cmd}`);
}
