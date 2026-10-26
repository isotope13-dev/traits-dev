// Static regression only. Do not execute.
package sample
import (wire "net/http"; system "os"; "strings")
func read(name string) string { return system.Getenv(name) }
func run() {
    read("DEPLOY_API_KEY")
    wire.Post("https://collector.invalid", "text/plain", strings.NewReader(read("PUBLIC_SETTING")))
}
