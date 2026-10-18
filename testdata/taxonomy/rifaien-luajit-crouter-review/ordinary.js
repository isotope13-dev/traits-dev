import { fetch } from './git.js';
export const check = mkt => fetch(mkt.root, mkt.ref);
export const normalize = value => value.split(separator).join('/');
export const evict = map => {
  let it = map.entries().next();
  map.delete(it.value[0]);
  return map.entries().next();
};
export const help = 'Search for files by glob pattern';
// Callers always respond with a generic HTTP status.
// Cancellation must not masquerade as a human-submitted result.
export const flags = params.filter(p => p.kind === 'flag');
