function handleRightClick(e) {
  if (e.which == 3) {
    window.location.replace('https://example.org/landing');
    return false;
  }
}
document.oncontextmenu = handleRightClick;
