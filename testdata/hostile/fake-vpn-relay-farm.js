/* fake-VPN service worker — probe for the raw-IP relay-farm composite */
const SERVERS = [
  { id: "us-1", host: "103.35.189.225", port: 1082, premium: false },
  { id: "de-1", host: "80.92.204.33", port: 1082, premium: true },
  { id: "de-2", host: "80.92.204.47", port: 1082, premium: true },
  { id: "gb-1", host: "5.180.30.122", port: 1082, premium: true },
  { id: "fr-1", host: "86.104.74.110", port: 1082, premium: true },
  { id: "nl-1", host: "194.150.220.163", port: 1082, premium: true }
];
const BYPASS = ["localhost", "127.0.0.1", "<-loopback>"];

function armShield(node) {
  const config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: { scheme: "socks5", host: node.host, port: node.port },
      bypassList: BYPASS
    }
  };
  chrome.proxy.settings.set({ value: config, scope: "regular" }, () => {
    chrome.action.setBadgeText({ text: "ON" });
  });
}

chrome.runtime.onMessage.addListener((msg, _s, send) => {
  if (msg.act === "arm") {
    const node = SERVERS.find(s => s.id === msg.nodeId);
    armShield(node);
    send({ ok: true });
  }
});
