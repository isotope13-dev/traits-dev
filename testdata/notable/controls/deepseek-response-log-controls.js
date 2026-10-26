// Benign control: DeepSeek API response logging in a dev client.
//
// Pins the relocated console-log leg: the deepseek-response-console-logging
// composite must still resolve now that console-log-response-text-call lives
// under micro-behaviors/os/console/io.
const INCOMING_DEEPSEEK_RESPONSE = "INCOMING DEEPSEEK RESPONSE";

export async function logDeepseekReply(data) {
  console.log(INCOMING_DEEPSEEK_RESPONSE, data.text);
  return data.text;
}
