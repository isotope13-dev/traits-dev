package controls

import "net"

// grpc.Dial("example.invalid:443") is documentation, not a call.
var example = `grpc.DialContext(ctx, target)`
var listenerFactory = net.Listen

// listener.Accept() is documentation, not a call.
type visitorNode interface { Accept(any) }
func visit(node visitorNode, visitor any) { node.Accept(visitor) }
