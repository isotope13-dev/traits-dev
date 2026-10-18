package fixture

import "fmt"
import _ "github.com/dimiro1/banner/autoload"

func main() {
    go agent.APIServer()
    agent.Shell()
    fmt.Println("getPublicKeysPowerShell()")
}
