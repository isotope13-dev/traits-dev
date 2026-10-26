package main

import (
    "net/http"
    "net/url"
    "os"
    "strings"
)

func main() {
    cuentas := strings.Split(os.Getenv("ACCOUNTS"), ",")
    claves := strings.Split(os.Getenv("CANDIDATES"), ",")
    endpoint := "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
    clave := claves[0]
    cuenta := cuentas[0]
    {
        {
            formulario := url.Values{}
            formulario.Set("grant_type", "password")
            formulario.Set("client_id", os.Getenv("CLIENT_ID"))
            formulario.Set("scope", "https://graph.microsoft.com/.default")
            formulario.Set("username", cuenta)
            formulario.Set("password", clave)
            respuesta, err := http.PostForm(endpoint, formulario)
            if err == nil {
                respuesta.Body.Close()
            }
        }
    }
}
