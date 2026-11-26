
// Helper for controlled input in web app, no extension APIs and no terms literal
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
function fillForm(el, val) {
  setter.call(el, val);
  document.querySelector("button[type=\"submit\"]").click();
}
