package main

import "net/http"

func main() {
	http.Get("https://update.googleapi.com/v1/beacon")
}
