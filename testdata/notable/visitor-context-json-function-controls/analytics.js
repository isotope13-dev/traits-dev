// page analytics beacon
var payload = { page: location.pathname, ref: document.referrer, host: location.hostname };
fetch("/api/track", { method: "POST", body: JSON.stringify(payload) }).then(function (r) { return r.json(); }).then(function (cfg) {
  var data = JSON.parse(localStorage.getItem("cfg") || "{}");
  data.last = cfg.ts; localStorage.setItem("cfg", JSON.stringify(data));
});
