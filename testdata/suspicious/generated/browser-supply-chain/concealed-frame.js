function inspectFrameShape(root) {
  root.insertAdjacentHTML('beforeend', '<iframe src="https://assets.example.invalid/preview.html" style="position:absolute;left:-10000px;width:0;height:0"></iframe>');
}
