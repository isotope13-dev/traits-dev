package controls

// tls.Client(conn, cfg), tls.NewListener(listener, cfg),
// http2.NewFramer(writer, reader), and syscall.Unlink(path) are examples.
var examples = []string{
	"tls.Client(conn, cfg)",
	"tls.NewListener(listener, cfg)",
	"http2.NewFramer(writer, reader)",
	"syscall.Unlink(path)",
}

// Neither a method declaration nor another receiver is the API call.
type fake struct{}

func (fake) NewListener() {}
func (fake) NewFramer()   {}
func (fake) Unlink()      {}

func unrelated(f fake) {
	f.NewListener()
	f.NewFramer()
	f.Unlink()
}
