const target = new URL("https://example.org/search");
new URLSearchParams(location.search).forEach(function(value, key) {
  target.searchParams.append(key, value);
});
window.location.replace(target.toString());
