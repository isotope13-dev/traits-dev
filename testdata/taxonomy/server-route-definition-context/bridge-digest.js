// An agent-chat transcript fold: `key` is a tool-argument digest on a
// message object, not a keystroke from a keyboard event.
function fold(events) {
  const acts = [];
  for (const e of events) {
    if (e.kind === "tool") {
      const prev = acts[acts.length - 1];
      if (prev && prev.call === e.call && prev.key && e.key && prev.key === e.key) {
        prev.n = (prev.n || 1) + 1;
      } else {
        acts.push({ call: e.call, note: e.args || "", key: e.key || "", ok: true });
      }
    }
  }
  return acts;
}
