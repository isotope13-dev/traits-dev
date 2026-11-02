const buffers = [Float32Array, Uint16Array];
const typed = new (buffers[selectBufferType(source.data)])(size);
