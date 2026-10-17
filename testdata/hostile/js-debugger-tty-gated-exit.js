const opts = process.env.NODE_OPTIONS || '';
if (opts.includes('--inspect') || process.argv.join(' ').includes('--inspect') || !process.stdout.isTTY) {
  process.exit(0);
}
console.log('payload runs only in an interactive, undebugged terminal');
