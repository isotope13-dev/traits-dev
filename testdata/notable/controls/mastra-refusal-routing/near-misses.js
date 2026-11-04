const schema = ordinaryConfig;
const method = "readMetadata";
const tokens = "one/two/three";
const diagnostics = [{ severity: 2 }, { severity: 3 }];
const request = { action: "preview" };
const digest = createHash("sha1").update("cache-key").digest("hex");
if (digest !== expected) console.log("cache miss");
