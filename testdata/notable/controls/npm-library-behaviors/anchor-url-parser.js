export function parseURL(url) {
  const location = document.createElement('a');
  location.href = url;
  return location.hostname;
}
