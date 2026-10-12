const preload="safe-delete.cjs";
const key="NODE_OPTIONS";
export function inspect(env){return {key,value:env[key],preload};}
