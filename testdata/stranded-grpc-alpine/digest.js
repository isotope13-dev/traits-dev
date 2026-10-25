const crypto = require("crypto");
const sum = crypto.createHash("sha256").update("passphrase").digest();
