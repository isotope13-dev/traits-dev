// Tutorial output: the step names a parameter, it does not print a key.
function printCloseHint(address) {
  console.log("sdk.hyperLiquid.hlCloseAll(address, privateKey)");
  console.log("This closes ALL positions immediately.");
}

module.exports = { printCloseHint };
