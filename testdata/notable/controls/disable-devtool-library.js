// Vendored DisableDevtool library (UMD): its Size detector probes the
// viewport delta. The library identity is the notable fact here; the
// anti-analysis probe atom must not re-report the library's own code.
(function (global) {
  global.DisableDevtool = function () {
    if (200 < window.outerWidth - window.innerWidth) return true;
    if (300 < window.outerHeight - window.innerHeight) return true;
    return false;
  };
})(window);
