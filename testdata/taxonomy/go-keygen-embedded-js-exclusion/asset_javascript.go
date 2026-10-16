//go:build embeddedjs

package main

import _ "embed"

//go:embed asset/embedded.js
var bundle string
