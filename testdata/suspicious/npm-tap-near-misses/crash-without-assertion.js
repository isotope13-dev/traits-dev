var test = require("tap").test
process.kill(process.pid, "SIGSEGV")
