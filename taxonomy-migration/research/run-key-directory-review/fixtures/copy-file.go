package main

//go:noinline
func copyFile(path string) string {
    return path + "/copied"
}

func main() { println(copyFile("file")) }
