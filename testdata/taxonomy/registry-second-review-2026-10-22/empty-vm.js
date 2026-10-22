const vm = require("node:vm"); const context = vm.createContext(); vm.runInContext("1 + 1", context);
