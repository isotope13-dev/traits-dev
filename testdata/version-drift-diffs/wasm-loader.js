const bytes = Uint8Array.from(atob("AGFzbQEAAAA="), c => c.charCodeAt(0));
const module = new WebAssembly.Module(bytes);
const instance = new WebAssembly.Instance(module);
