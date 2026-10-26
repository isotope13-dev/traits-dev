// Benign compatibility probe: parses the Chrome version for a feature
// gate but never labels any branch vulnerable, so the version-branch
// trait must stay silent here.
var ua = navigator.userAgent;
var cm = ua.match(/Chrome\/(\d+)\.(\d+)\.(\d+)\.(\d+)/);
if (!cm) {
  report('not-chrome');
} else {
  var major = parseInt(cm[1], 10);
  var ok = (major >= 100);
  report('Chrome ' + cm[0] + (ok ? ' - SUPPORTED' : ' - UNSUPPORTED'));
}
