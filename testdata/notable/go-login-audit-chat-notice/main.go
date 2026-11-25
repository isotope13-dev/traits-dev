package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
)

type loginEvent struct {
	Username string `json:"username"`
	Password string `json:"password"`
	IP       string `json:"ip"`
}

func sendTelegram(token, chatID, text string) error {
	url := "https://api.telegram.org/bot" + token + "/sendMessage"
	body, _ := json.Marshal(map[string]string{"chat_id": chatID, "text": text})
	resp, err := http.Post(url, "application/json", bytes.NewReader(body))
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	return nil
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	var ev loginEvent
	if err := json.NewDecoder(r.Body).Decode(&ev); err != nil {
		http.Error(w, "bad", http.StatusBadRequest)
		return
	}
	// Audit line: the password is verified upstream and never forwarded.
	_ = sendTelegram(os.Getenv("BOT_TOKEN"), os.Getenv("CHAT_ID"), "login by "+ev.Username+" from "+ev.IP)
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	http.HandleFunc("/login", loginHandler)
	_ = http.ListenAndServe(":8080", nil)
}
