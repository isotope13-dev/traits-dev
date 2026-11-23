package example
import "os"
func report() string {
 home, _ := os.UserHomeDir()
 return home
}
