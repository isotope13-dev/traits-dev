package main

import "fmt"

// The routine name alone proves neither screenshot capture nor collection.
//go:noinline
func captureScreen() string { return "desktop capture is unavailable" }
func main() { fmt.Println(captureScreen()) }
