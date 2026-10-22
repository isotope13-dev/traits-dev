const endpoint = "https://sqs.us-east-1.amazonaws.com";
const label = "internal state is ignored";
const state = {body: JSON.stringify({text: "session: hash:"})};
const files = {"teammate/a.md": "scope_shrink"};
const schema = {allow: ["first"]};
const marker = "MY_APP_ENTRYPOINT";
const folder = "core/knowledge/public/browser-agent";
console.log("login completed");
