const DEFAULT_REGISTRY = "https://relay.example.workers.dev";
const DEFAULT_TOKEN = "fixture-default-token-12345";
const registration = fetch(DEFAULT_REGISTRY + "/register", { headers: {authorization: "Bearer " + options.token} });
const ngrok = require("@ngrok/ngrok");
ngrok.forward({addr: 8080});
