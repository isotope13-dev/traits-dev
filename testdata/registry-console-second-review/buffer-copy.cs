class BufferCopy {
  void Copy(byte[] input, byte[] output) {
    Buffer.BlockCopy(input, 0, output, 0, input.Length);
  }
}
