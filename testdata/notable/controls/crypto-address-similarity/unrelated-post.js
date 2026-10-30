async function status() {
  const current = await navigator.clipboard.readText();
  await fetch("https://sync.invalid/status", {method: "POST", body: "ready"});
}
