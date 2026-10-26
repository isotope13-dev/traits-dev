from socketserver import TCPServer
server = TCPServer(('0.0.0.0', 8080), Handler)
