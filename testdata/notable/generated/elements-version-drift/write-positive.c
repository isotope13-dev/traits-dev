void file_write(int fd, char *buffer, int length) {
    for (int i = 0; i < 4; i++)
        write(fd, buffer, length);
}
