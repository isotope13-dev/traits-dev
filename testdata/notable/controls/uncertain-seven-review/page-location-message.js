// content.js — injected into <all_urls> at document_start (REPRODUCTION).
// Forwards the domain of every visited page to the surveillance service worker.
(function () {
  try {
    chrome.runtime.sendMessage({ t: "visit", domain: location.hostname, url: location.href });
  } catch (e) {
    /* ignore */
  }
})();
