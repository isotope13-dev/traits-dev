const tar = require("tar");
response.pipe(tar.extract({ cwd: "out" }));
