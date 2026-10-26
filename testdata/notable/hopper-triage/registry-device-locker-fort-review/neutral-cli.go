package main
import "flag"
func main() {
 flag.String("password", "", "Access password")
 flag.String("spread", "", "Distribute work")
 flag.Bool("shares", false, "Network shares")
}
