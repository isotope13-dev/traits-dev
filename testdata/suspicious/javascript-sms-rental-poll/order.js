const base = "https://sms.example.test";
const order = await fetch(base + "/v1/user/buy/activation/any/any/any");
const code = await fetch(base + "/v1/user/check/12345");
console.log(code);
