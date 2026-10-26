import https from "https";

// Ordinary verified fetch: no rejectUnauthorized anywhere, so neither the
// bypass atom nor anything built on it may fire.
const req = https.get("https://updates.example.com/v1", (res) => {
  res.resume();
});
req.on("error", () => {});
