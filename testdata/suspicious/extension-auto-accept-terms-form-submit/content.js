
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
chrome.storage.local.get(["userId"], (d) => {
  const cb = document.getElementById("acceptTerms");
  cb.click();
  document.querySelector("button[type=\"submit\"]").click();
});
