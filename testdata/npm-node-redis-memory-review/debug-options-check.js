export function attached() {
  return process.env.NODE_OPTIONS?.includes('--inspect') || process.argv.some(a => a.includes('--inspect'));
}
