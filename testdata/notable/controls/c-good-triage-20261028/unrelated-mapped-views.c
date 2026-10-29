void copy(void *src_handle, void *dst_handle, void *other_src, void *other_dst) {
  void *src = MapViewOfFile(src_handle, FILE_MAP_READ, 0, 0, 4096);
  void *dst = MapViewOfFile(dst_handle, FILE_MAP_WRITE, 0, 0, 4096);
  memmove(other_dst, other_src, 4096);
  FlushViewOfFile(dst, 4096);
}
