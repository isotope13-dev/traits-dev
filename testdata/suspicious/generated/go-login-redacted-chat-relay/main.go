package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
)

type loginEvent map[string]interface{}

var masked = map[string]bool{"password": true, "token": true}

func getMap(m map[string]interface{}, key string) map[string]interface{} {
	v, _ := m[key].(map[string]interface{})
	return v
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
	if r.Method != http.MethodPost {
		http.Error(w, "method", http.StatusMethodNotAllowed)
		return
	}
	var payload loginEvent
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "bad", http.StatusBadRequest)
		return
	}
	username, _ := payload["username"].(string)
	password := "[redacted]"
	device := getMap(payload, "device")
	screen := getMap(device, "screen")
	w2 := fmt.Sprint(screen["width"])
	h2 := fmt.Sprint(screen["height"])
	text := fmt.Sprintf("user=%s pass=%s os=%v screen=%s x %s",
		username, "[redacted]", device["platform"], w2, h2)
	_ = sendTelegram(os.Getenv("BOT_TOKEN"), os.Getenv("CHAT_ID"), text)
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/login", loginHandler)
	srv := &http.Server{Addr: ":8080", Handler: mux}
	_ = strconv.Itoa(len(masked))
	_ = srv.ListenAndServe()
}
