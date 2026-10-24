const chromeArgs = ["--remote-debugging-port=9222", "--user-data-dir=/tmp/browser", "--disable-component-update"];
const clipboard = {expression: "navigator.clipboard.readText()"};
await session.send("Page.captureScreenshot", {});
const headers = {"Upload-Offset": "0"};
const field = "mcp_tool_use";
const threshold = "HarmBlockThreshold";
const requirement = "Tool approval is required before execution";
