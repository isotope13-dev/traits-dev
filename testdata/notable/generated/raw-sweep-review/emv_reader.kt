fun readRecord(sfi: Int, record: Int): ByteArray =
    byteArrayOf(0x00, 0xB2.toByte(), record.toByte(), ((sfi shl 3) or 4).toByte(), 0x00)
