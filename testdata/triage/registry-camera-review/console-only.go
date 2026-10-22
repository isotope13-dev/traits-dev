package camera
func help(c *Client) {
 c.Call("console.runCmd", map[string]any{"command": "help"}, 1, nil, nil)
}
