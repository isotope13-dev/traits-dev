class EmvReader {
    byte[] readRecord(int sfi, int record) {
        return new byte[] {(byte) 0x00, (byte) 0xB2, (byte) record, (byte) ((sfi << 3) | 4), 0x00};
    }
}
