function bindLegacy(element, listener) {
  element.attachEvent("onclick", listener);
  element.detachEvent("onclick", listener);
  return window.event.target;
}
