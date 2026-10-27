package demo
import("context"; "os"; "os/exec")
func run(ctx context.Context) error {
 return exec.CommandContext(ctx, "git", "-c", "core.hooksPath=" + os.DevNull, "status").Run()
}
