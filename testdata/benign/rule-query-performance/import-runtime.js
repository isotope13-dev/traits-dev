// An unrelated chained call must not hide a runtime import in this declaration.
const loaded = [Promise.resolve().then(() => 1), import('runtime-package')];
