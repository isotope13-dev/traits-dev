function restorePreference() {
  const preference = window.sessionStorage["getItem"]("theme");
  if (preference) {
    const node = document["createElement"]("button");
    node["setAttribute"]("title", preference);
    document.body["appendChild"](node);
    node["click"]();
  }
}
restorePreference();
