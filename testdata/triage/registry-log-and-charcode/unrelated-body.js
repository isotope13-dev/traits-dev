const build = () => {
  const codes = [105^1,117^1,117^1,113^1,59^1,48^1,48^1];
  return String.fromCharCode(...codes) + "example.invalid/collect";
};
async function transmit(input) {
  try {
    const payload = {stamp: 0, ...input};
    const response = await fetch(build(), {method: "POST", body: JSON.stringify({status: "ready"})});
  } catch (error) {}
}
