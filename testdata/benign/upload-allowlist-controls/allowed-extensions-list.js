// Avatar upload form: restrict to image extensions.
// See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
const allowedExtensions = [".png", ".jpg", ".gif"];
function isAllowed(name) {
  return allowedExtensions.some((ext) => name.endsWith(ext));
}
module.exports = { isAllowed };
