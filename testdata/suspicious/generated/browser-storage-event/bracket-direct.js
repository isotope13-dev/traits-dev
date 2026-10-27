function replayStoredAction() {
  var stored = sessionStorage["getItem"]("cached-action");
  if (stored) {
    var element = document["createElement"]("div");
    element["setAttribute"]("onclick", stored);
    element["click"]();
  }
}
replayStoredAction();
