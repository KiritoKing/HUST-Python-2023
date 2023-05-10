from http.server import HTTPServer, SimpleHTTPRequestHandler as RH
from functools import partial
import threading


class Server(threading.Thread):
    def __init__(self, port: int, path: str = "shared") -> None:
        super().__init__()
        self.dir = path
        RH.extensions_map = {k: v + ';charset=UTF-8' for k, v in RH.extensions_map.items()}
        handler = partial(RH, directory=path)
        self.server = HTTPServer(('0.0.0.0', port), handler)
        self.runing = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def stop(self):
        self.server.shutdown()
        self.runing = False

    def run(self):
        print(f'server start on port {self.server.server_port}')
        self.server.serve_forever()
        self.runing = True


if __name__ == '__main__':
    handler = partial(SimpleHTTPRequestHandler, directory='d:\\')
    server = HTTPServer(('0.0.0.0', 8888), handler)
    server.serve_forever()
