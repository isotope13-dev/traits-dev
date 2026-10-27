function restoreButton(action, replacement) {
  const stored = localStorage["getItem"]("theme");
  if (stored) {
    let node = document["createElement"]("button");
    node["setAttribute"]("onclick", action);
    node = replacement;
    node["click"]();
  }
}
restoreButton("window.print()", document.querySelector("button"));
