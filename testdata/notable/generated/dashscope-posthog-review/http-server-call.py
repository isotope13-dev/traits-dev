server = HTTPServer(('127.0.0.1', 8080), Handler)
threaded = http.server.ThreadingHTTPServer(('127.0.0.1', 8081), Handler)
