package main
type Server struct{}
func(s *Server) Start(){}
func main(){server:= &Server{}; server.Start()}
