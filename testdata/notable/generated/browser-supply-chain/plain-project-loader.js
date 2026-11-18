const project = {projectJS: function () {
  const resource = document.createElement('script');
  resource.src = 'https://assets.example.invalid/example.js';
  document.head.appendChild(resource);
}};
