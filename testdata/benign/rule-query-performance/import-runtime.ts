// Runtime imports still load modules in files that also use import types.
type Factory = Wrap<typeof import('type-package')>;
const loaded = import('runtime-package');
