package checks

import (
    "net"
    "time"
    "github.com/cespare/xxhash/v2"
)

func probe(network, address string) {
    net.DialTimeout(network, address, time.Second)
    net.DialTimeout("tcp", address, time.Second)
    xxhash.Sum64String(address)
}
