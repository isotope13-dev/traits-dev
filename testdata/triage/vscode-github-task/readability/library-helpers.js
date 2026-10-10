const alpha = n => String.fromCharCode(97+n);
const record = value => ({data:Buffer.from(value)});
const logPath = "daemon.log";
const cache = Math.random() < 0.1 ? "./remove-old-cache-records.js" : "";
function parent(path) { return path.length===1 && path.charCodeAt(0)===46 ? "" : path; }
const normalizePath = (str, stripTrailing) => str.replace(/\\/g, "/");
var Apn=/^\/\/\/?\s*@(ts-expect-error|ts-ignore)/;
const detectContainer = () => { try { return fs.statSync("/run/.containerenv"); } catch { return false; } };
const syntaxKind = node => node.kind === 322 ? node.text : "";
