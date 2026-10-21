// Computed reads still expose an observable display-property collection.
export function dimensions() {
  return { width: screen[getProperty(0)], height: screen[getProperty(1)] };
}
