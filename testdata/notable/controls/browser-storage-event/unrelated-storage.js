function bindAction(action) {
  const preference = localStorage["getItem"]("theme");
  if (preference) {
    const node = document["createElement"]("button");
    node["setAttribute"]("onclick", action);
    document.body["appendChild"](node);
    node.addEventListener("focus", () => console.log(preference));
  }
}
bindAction("window.print()");
