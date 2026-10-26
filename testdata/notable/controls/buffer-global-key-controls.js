// global[Buffer.from([68, 97, 116, 101])]
const example = "global[Buffer.from([68, 97, 116, 101])]";
const date = global[Buffer.from('Date')];
const bytes = Buffer.from([68, 97, 116, 101]);
const ordinary = object[Buffer.from([68, 97, 116, 101])];
const other = global[Codec.from([68, 97, 116, 101])];
const allocated = global[Buffer.alloc([68, 97, 116, 101])];
