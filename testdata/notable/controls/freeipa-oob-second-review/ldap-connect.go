package main
import "github.com/go-ldap/ldap/v3"
func main() {
    conn, err := ldap.DialURL("ldap://directory.example")
    if err == nil { conn.Close() }
}
