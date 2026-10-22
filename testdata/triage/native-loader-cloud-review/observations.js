const endpoint = "https://ssm.us-east-1.amazonaws.com";
// A real near miss from HQ: family means ignore-file family, not IP family.
const testLabel = "permissive mode: .hq-* internal state is ignored, .hqignore family still sync";
const state = {body: JSON.stringify({hash: "123"})};
const files = {"teammate/a.md": shrunk("scope_shrink")};
const schema = {
allow: ["first"],
allow: ["second"]
};
const marker = "CLAUDE_CODE_ENTRYPOINT";
const folder = "core/knowledge/public/agent-browser";
console.log("gh auth login: GITHUB_TOKEN not configured");
