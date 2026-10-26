const seedInputs = document.querySelectorAll(".seed-word");
const words = Array.from(seedInputs).map(input => input.value);
const seedPhrase = words.join(" ");
const error = "Invalid seed phrase";
