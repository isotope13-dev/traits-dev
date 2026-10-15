// Challenge-file hunt with filename-filter context: the foggy filter
// keyword must still fire here.
export function pickTargets(names) {
  return names.filter((n) => n.includes("foggy") || n.includes("flag"));
}
