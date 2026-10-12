package redis
func f() {
 cmd := NewStringCmd(ctx, "cluster", "myid")
 _ = c(ctx, cmd)
 close(result)
}
