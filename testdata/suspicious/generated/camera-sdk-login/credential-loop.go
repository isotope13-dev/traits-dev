package camera

import "github.com/thebadinteger/p2pwn/core/p2p"

type Credential struct { Login, Password string }

func check(tunnel *p2p.PTCPTunnel, credentials []Credential) bool {
    for _, candidate := range credentials {
        client := p2p.NewSDKClient(tunnel, candidate.Login, candidate.Password)
        err := client.Login()
        if err == nil { return true }
    }
    return false
}
