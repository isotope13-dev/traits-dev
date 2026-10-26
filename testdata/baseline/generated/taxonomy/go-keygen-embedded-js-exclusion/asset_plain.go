//go:build !embeddedjs

package main

import _ "embed"

//go:embed asset/neutral.txt
var bundle string
