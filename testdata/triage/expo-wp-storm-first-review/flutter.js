const plugin = "webview_flutter_wkwebview";
const message = "A JavaScriptChannel with name `channel`";
function send(channel, data) { channel.postMessage(JSON.stringify(data)); }
