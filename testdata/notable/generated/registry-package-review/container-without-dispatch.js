/*! Exegol Studio v1.0.0 */
const cp = require("child_process");
const prompt = "A professional pentest image ships a broad offensive-security toolset";
const tool = {id:"exec",description:"Execute a shell command inside the container.",execute(e,t){return Promise.resolve({stdout:""});}};
const argv = ["exec","-i",...cfg.envArgs,"--",cfg.containerId,"zsh"];
(0,cp.spawn)("docker",argv);
const graph = {id:"save_killchain"};
const docs = {pagesFile:"patt-pages.json"};
