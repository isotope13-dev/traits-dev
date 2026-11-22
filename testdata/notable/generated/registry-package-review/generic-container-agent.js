const cp = require("child_process");
const prompt = "A professional pentest image ships a broad offensive-security toolset";
const tool = {id:"exec",description:"Execute a shell command inside the container.",execute(e,t){return t.executor.exec(n,e.command,{cwd:e.workdir});}};
const argv = ["exec","-i",...cfg.envArgs,"--",cfg.containerId,"zsh"];
(0,cp.spawn)("docker",argv);
const graph = {id:"save_killchain"};
const docs = {pagesFile:"patt-pages.json"};
