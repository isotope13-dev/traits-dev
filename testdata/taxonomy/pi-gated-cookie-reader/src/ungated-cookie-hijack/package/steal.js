// Static cookie-query and RPC constants; this fixture performs no reads or requests.
const query =
  "SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%google%'";
const endpoint =
  "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate";

module.exports = { query, endpoint };
