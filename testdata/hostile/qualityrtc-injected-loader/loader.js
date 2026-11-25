var n = {};
function qrtcRun(e) {
  var codeUrl = 'https://qualityrtc-sdk.s3.amazonaws.com/1.0/main.bundle.js';
  var configUrl = e.configUrl + '/get-qualityrtc-config';
  return fetch(configUrl).then(function (r) { return r.json(); });
}
function qrtcStop() {}
module.exports = { api: { qualityrtc: { run: n.qrtcRun, stop: n.qrtcStop } }, qrtcRun: qrtcRun, qrtcStop: qrtcStop };
