package main
import ("net"; "os")
func main() { net.LookupHost(os.Getenv("SERVICE_HOST")) }
