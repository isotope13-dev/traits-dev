import fs from "node:fs";
const apiKey = process.env.OPENAI_API_KEY;
const body = fs.readFileSync("prompt.txt", "utf8");
fetch("https://api.openai.com/v1/chat/completions", {
  method: "POST",
  headers: { Authorization: "Bearer " + apiKey },
  body: JSON.stringify({ messages: [{ role: "user", content: body }] }),
});
