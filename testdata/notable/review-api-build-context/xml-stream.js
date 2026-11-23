function configure(writer, options) {
  writer.on("data", options.data);
  writer.on("end", options.end);
  return writer;
}
function next(e) { return e.state.first; }
