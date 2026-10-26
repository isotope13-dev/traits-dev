export default {transformIndexHtml() {
  return [{tag: "script", attrs: {src: "/widget.js"}, injectTo: "head"}];
}};
