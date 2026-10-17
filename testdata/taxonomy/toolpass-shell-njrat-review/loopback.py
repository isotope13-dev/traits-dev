from socketserver import TCPServer
server = TCPServer(('127.0.0.1', 8080), Handler)
