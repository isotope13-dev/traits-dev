chrome.tabs.captureVisibleTab(1, {format: "jpeg"}).then(image => {
  socket && socket.readyState === WebSocket.OPEN &&
    socket.send(JSON.stringify({type: "frame", data: image}));
});
