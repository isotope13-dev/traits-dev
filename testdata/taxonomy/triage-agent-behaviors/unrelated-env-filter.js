const env={...process.env};
const key="NODE_OPTIONS";
const pattern=/--inspect/;
const cleaned=env[key].replace(pattern, "");
if(cleaned)env[key]=cleaned;else delete env[key];
