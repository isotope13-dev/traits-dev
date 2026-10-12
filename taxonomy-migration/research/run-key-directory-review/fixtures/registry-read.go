package main

import "golang.org/x/sys/windows/registry"

func main() {
    key, _ := registry.OpenKey(registry.CURRENT_USER, `Software\Microsoft\Windows\CurrentVersion\Run`, registry.READ)
    defer key.Close()
}
