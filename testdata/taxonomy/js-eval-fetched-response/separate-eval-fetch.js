const cache = {};
async function getJson(url) {
  const response = await fetch(url);
  return response.json();
}
function run(code) {
  window["eval"](code);
}
