async function operate() {
  const output = process.env.OUT_DIR;
  console.log(output);
  await fetch("https://collector.example.invalid/submit", {method: "POST", body: "build_started"});
}
if (false) operate();
