package scanner

import "github.com/JustinTimperio/gomap"

func inspect() {
 for port := 1; port < 100; port++ { _ = port }
 gomap.Scan()
}
