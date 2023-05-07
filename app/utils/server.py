from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

if __name__ == '__main__':
    handler = partial(SimpleHTTPRequestHandler, directory='d:\\')
    server = HTTPServer(('0.0.0.0', 8888), handler)
    server.serve_forever()
