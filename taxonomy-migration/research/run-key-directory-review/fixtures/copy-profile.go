package main

//go:noinline
func cloneBrowserProfile(path string) string {
    return path + "/copied"
}

func main() { println(cloneBrowserProfile("profile")) }
