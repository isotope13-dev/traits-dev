export function annotateTrace(entry, tracePath) {
  entry.span.setAttribute("test.trace.path", tracePath);
}
