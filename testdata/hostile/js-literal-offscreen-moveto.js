// True-positive control for window-offscreen-resize: a literal moveTo
// parking the window at a far off-desktop coordinate. The two-digit
// negative / large-second-coordinate legs must keep firing here.
window.moveTo(1,9999);
