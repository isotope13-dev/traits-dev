// Layout-object dimensions do not establish browser screen access.
export function dimensions(layout) {
  return { width: layout[getProperty(0)], height: layout[getProperty(1)] };
}
