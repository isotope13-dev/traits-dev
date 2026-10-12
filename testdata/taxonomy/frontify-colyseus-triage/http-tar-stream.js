const https = require("https");
const tar = require("tar");
const fs = require("fs");
https.get("https://example.org/archive.tgz", response => { response.pipe(tar.x()); response.pipe(fs.createWriteStream("archive.tgz")); });
