// Excerpts of the inactive implementation in @workbench-stack/core 3.5.0.
// const win = new BrowserWindow({show: true});
// const args = process.argv;
// const target = `https://example.invalid/?data=${encodeURIComponent(args)}`;
// chrome.webRequest.onBeforeRequest.addListener(() => { return {cancel: true}; });
// chrome.webRequest.onBeforeSendHeaders.addListener(() => { return {cancel: false}; });
// win.webContents.session.webRequest.onBeforeRequest((details, callback) => {
//   callback({cancel: true});
// });
