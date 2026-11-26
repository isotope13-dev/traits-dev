// Synthetic fixture: page-world hooks that count requests and post a counter.
// The posted value is a number, not the request body, so this is co-occurrence only.
(() => {
  let sent = 0;
  const nativeFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    sent += 1;
    window.postMessage({ source: "usage-counter", count: sent }, location.origin);
    return nativeFetch(input, init);
  };
  const XS = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function () {
    sent += 1;
    window.postMessage({ source: "usage-counter", count: sent }, location.origin);
    return XS.apply(this, arguments);
  };
})();
