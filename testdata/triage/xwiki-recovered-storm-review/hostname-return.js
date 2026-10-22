import {execSync} from "child_process";
function probe(){if(execSync("hostname").toString().toLowerCase().includes("sandbox")) return true;return false;}
