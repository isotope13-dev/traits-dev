package camera
import ("image/jpeg"; "fmt")
func TryCVE2025Probe() {
 _ = jpeg.DefaultQuality
 request := `{"session":0}`
 snapshot := "/cgi-bin/snapshot.cgi"
 config := "/cgi-bin/configManager.cgi?action=getConfig"
 add := "/cgi-bin/userManager.cgi?action=addUser&user.Group=admin"
 path := fmt.Sprintf("%s_%s_%s_%s.jpg", "serial", "user", "password", "model")
 _, _, _, _, _ = request, snapshot, config, add, path
}
