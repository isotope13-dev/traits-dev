import {execSync} from "child_process";
console.log(execSync("hostname").toString().includes("sandbox"));
