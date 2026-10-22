const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
export function compile(code) {
  return new AsyncFunction("value", code);
}
