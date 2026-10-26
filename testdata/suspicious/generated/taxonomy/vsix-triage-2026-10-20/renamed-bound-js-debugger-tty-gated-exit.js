const runtimeFlags = process.env.NODE_OPTIONS || '';
if (runtimeFlags.includes('--inspect') || process.argv.join(' ').includes('--inspect') || !process.stdout.isTTY) {
  process.exit(0);
}
console.log('payload runs only in an interactive, undebugged terminal');
