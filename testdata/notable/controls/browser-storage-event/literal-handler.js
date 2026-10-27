function printPage() {
  const node = document["createElement"]("button");
  node["setAttribute"]("onclick", "window.print()");
  node["click"]();
}
printPage();
