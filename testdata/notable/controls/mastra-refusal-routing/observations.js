// API/configuration references do not identify another product or an attack.
const schema = mcpServerConfigSchema;
const method = "readFile";
const tokens = "[^\\S\\n\\r]";
const diagnostics = [{ severity: "error" }, { severity: "warning" }];
const request = { action: "execute" };
const digest = createHash("sha256").update("cache-key").digest("hex");
if (digest !== expected) console.log("cache miss");
