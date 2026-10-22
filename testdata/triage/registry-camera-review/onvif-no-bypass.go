package camera
func dump(c *Client) {
 commands := []string{"OnvifUser -u"}
 for _, command := range commands {
  c.Call("console.runCmd", map[string]any{"command": command}, 2, nil, nil)
 }
}
