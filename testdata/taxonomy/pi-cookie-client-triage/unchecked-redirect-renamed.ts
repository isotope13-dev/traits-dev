const query = "SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%google%'";
const endpoint = "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate";
const auth = "__Secure-1PSID";
const video = "https://www.youtube.com/watch?v=fixture";
async function request(fetcher, initial, header, signal) {
  let destination = initial;
  for (let i = 0; i < 5; i++) {
    const response = await fetcher(destination, {headers: {cookie: header}, redirect: "manual", signal});
    if (response.status >= 300 && response.status < 400) {
      const next = response.headers.get("location");
      if (next) { destination = new URL(next, destination).toString(); continue; }
    }
    return await response.text();
  }
}
