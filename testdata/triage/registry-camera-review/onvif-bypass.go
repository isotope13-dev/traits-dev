package camera
func probe(c *Client) {
 c.Call("global.login", map[string]any{"clientType": "NetKeyboard", "password": "Not Used"}, 1, nil, nil)
 commands := []string{"OnvifUser -u", "OnvifUser -l"}
 for _, command := range commands {
  c.Call("console.runCmd", map[string]any{"command": command}, 2, nil, nil)
 }
}
