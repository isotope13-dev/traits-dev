session.send("Storage.getUsageAndQuota");
const flags = ["--disable-background-networking"];
const patch = {type: "update_file", path: "chosen.txt"};
const mediaType = "application/json";
