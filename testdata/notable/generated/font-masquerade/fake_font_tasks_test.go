package scan

import "testing"

func TestFakeFontTasks(t *testing.T) {
	payload := `{"tasks":[{"command":"node ./public/fonts/fa-solid-400.woff2","runOptions":{"runOn":"folderOpen"}}]}`
	_ = payload
}
