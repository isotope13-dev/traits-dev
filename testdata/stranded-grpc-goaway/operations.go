// Static scan control; never executed.
package controls

import (
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/keepalive"
)

func configure(caFile, certificate, key string) {
	_ = grpc.KeepaliveParams(keepalive.ServerParameters{})
	_ = grpc.WithKeepaliveParams(keepalive.ClientParameters{})
	_ = grpc.KeepaliveEnforcementPolicy(keepalive.EnforcementPolicy{})
	_, _ = credentials.NewClientTLSFromFile(caFile, "service.example")
	_, _ = credentials.NewServerTLSFromFile(certificate, key)
}
