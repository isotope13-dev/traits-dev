void copy(void *src_handle, void *dst_handle) {
  void *src = MapViewOfFile(src_handle, FILE_MAP_READ, 0, 0, 4096);
  void *dst = MapViewOfFile(dst_handle, FILE_MAP_WRITE, 0, 0, 4096);
  memmove(dst, src, 4096);
  FlushViewOfFile(dst, 4096);
}
