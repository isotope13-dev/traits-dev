const https = require("https");

https.get("https://api.telegram.org/botSTATUS/sendMessage", (response) => {
  response.resume();
});
