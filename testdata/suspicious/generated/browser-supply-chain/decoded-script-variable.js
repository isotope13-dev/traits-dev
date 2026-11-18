function loaderExample() {
  const address = window.atob('aHR0cHM6Ly9hc3NldHMuZXhhbXBsZS5pbnZhbGlkL2V4YW1wbGUuanM=');
  const resource = document.createElement('script');
  resource.src = address;
  document.head.appendChild(resource);
}
