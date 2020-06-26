import http.server as server
import socketserver

PORT = 8080

Handler = server.SimpleHTTPRequestHandler
Handler.extensions_map = {
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.css':	'text/css',
    '.js':	'application/x-javascript'
}


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f'serving at port{PORT}')
    httpd.serve_forever()
