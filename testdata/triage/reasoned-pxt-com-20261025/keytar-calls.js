const keytar = require("keytar");
keytar.getPassword("app", "user");
keytar.replacePassword("app", "user", "value");
keytar.deletePassword("app", "user");
