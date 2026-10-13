import * as disk from "node:fs";
disk.rmSync(tempDir, {"recursive":true, force:true});
