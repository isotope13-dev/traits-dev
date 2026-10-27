function configureButtons(action, other) {
  const node = document["createElement"]("button");
  node["setAttribute"]("onclick", action);
  other["click"]();
}
configureButtons("window.print()", document.querySelector("button"));
