// Fixture companion for the window-offscreen-resize triage
// (react-doctor 0.9.17-dev, benign): terminal list-widget keyboard
// navigation moves the *selection* by -1/+1 steps. Those small step
// arguments are list cursors, not off-desktop window coordinates, so the
// off-screen trait must stay silent here.
function useListNavigation({ itemCount, height, onSelect }) {
  let selectedIndex = 0;
  function moveTo(index, step) {
    selectedIndex = Math.max(0, Math.min(itemCount - 1, index));
    if (step !== 0) onSelect(selectedIndex);
  }
  function onKey(key, input) {
    if (key.downArrow || input === "j") return moveTo(selectedIndex + 1, 1);
    if (key.upArrow || input === "k") return moveTo(selectedIndex - 1, -1);
    if (key.pageDown) return moveTo(selectedIndex + height, 1);
    if (key.pageUp) return moveTo(selectedIndex - Math.floor(height / 2), -1);
    if (input === "G") return moveTo(itemCount - 1, -1);
  }
  return { onKey, moveTo };
}
module.exports = { useListNavigation };
