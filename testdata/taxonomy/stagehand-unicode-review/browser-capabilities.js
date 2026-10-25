session.send("Runtime.runIfWaitingForDebugger");
session.send("Storage.setCookies", {cookies: requested});
session.send("Storage.clearCookies");
const flags = ["--disable-client-side-phishing-detection"];
const patch = {type: "delete_file", path: "chosen.txt"};
const mediaType = "application/zip";
