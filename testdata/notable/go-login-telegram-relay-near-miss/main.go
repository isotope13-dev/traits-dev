package main

import (
	"encoding/json"
	"net/http"
)

// Login handler that checks the password locally; nothing leaves the host.
func loginHandler(w http.ResponseWriter, r *http.Request) {
	var payload map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "bad", http.StatusBadRequest)
		return
	}
	password, _ := payload["password"].(string)
	if password == "" {
		http.Error(w, "empty", http.StatusUnauthorized)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	http.HandleFunc("/login", loginHandler)
	_ = http.ListenAndServe(":8080", nil)
}
