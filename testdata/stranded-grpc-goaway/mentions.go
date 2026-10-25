// Static scan control; never executed.
package controls

// grpc.KeepaliveParams(keepalive.ServerParameters{})
// grpc.WithKeepaliveParams(keepalive.ClientParameters{})
// grpc.KeepaliveEnforcementPolicy(keepalive.EnforcementPolicy{})
// credentials.NewClientTLSFromFile("ca.pem", "service.example")
// credentials.NewServerTLSFromFile("server.pem", "key.pem")
var examples = []string{
	"grpc.KeepaliveParams(keepalive.ServerParameters{})",
	"grpc.WithKeepaliveParams(keepalive.ClientParameters{})",
	"grpc.KeepaliveEnforcementPolicy(keepalive.EnforcementPolicy{})",
	"credentials.NewClientTLSFromFile(ca, host)",
	"credentials.NewServerTLSFromFile(cert, key)",
}

func otherReceivers() {
	other.KeepaliveParams(nil)
	other.WithKeepaliveParams(nil)
	other.KeepaliveEnforcementPolicy(nil)
	other.NewClientTLSFromFile("ca.pem", "service.example")
	other.NewServerTLSFromFile("server.pem", "key.pem")
}
