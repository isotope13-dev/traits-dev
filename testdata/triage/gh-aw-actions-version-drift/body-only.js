const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
export const referenceBody = new AsyncFunction("require");
