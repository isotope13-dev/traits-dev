// CLI date-argument validation (cf. agentlog backfill.ts): set-then-verify
// against caller-supplied components checks the INPUT is a real calendar
// date; it asserts no environment-chosen constant, so it is not clock-hook
// (emulator) evasion.
export function parseDateArg(value) {
  const m = String(value).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!m) throw new Error("date must be YYYY-MM-DD");
  const year = Number(m[1]);
  const month = Number(m[2]);
  const day = Number(m[3]);
  const date = new Date(0);
  date.setFullYear(year, month - 1, day);
  date.setHours(0, 0, 0, 0);
  if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
    throw new Error("date must be a valid YYYY-MM-DD calendar date");
  }
  return date;
}
