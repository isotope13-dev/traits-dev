void stream_write(Stream &stream, char *buffer, int length) {
    for (int i = 0; i < 4; i++)
        stream.write(buffer, length);
}
