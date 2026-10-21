function parseFeed(nodes) {
  function fetch(tag, where, recurse) {
    return textContent(getElementsByTagName(tag, where, recurse, 1)).trim();
  }
  return fetch("summary", nodes);
}
fetch(url).then(r => r.text()).then(eval);
