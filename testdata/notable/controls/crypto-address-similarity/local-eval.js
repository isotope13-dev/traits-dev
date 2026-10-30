async function expression() {
  const response = await fetch("https://sync.invalid/status");
  const current = await response.text();
  eval("1 + 2".substring(0));
}
