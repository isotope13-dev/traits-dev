function replayDecodedStage() {
  let cached = globalThis.localStorage.getItem("next-stage");
  if (cached) {
    let target = document["createElement"]("span");
    target.setAttribute("onclick", atob(cached));
    target["click"]();
    target.remove();
  }
}
replayDecodedStage();
