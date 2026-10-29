package main

import "os/exec"

func main() {
    encodedStager := "stager.go"
    _ = exec.Command("go", "build", encodedStager)
}
