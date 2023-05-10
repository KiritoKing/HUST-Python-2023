from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial
import urllib.parse
import threading

class Utf8HTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # 设置响应头的Content-Type，指定编码为utf-8
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        super().end_headers()

    def translate_path(self, path):
        # 解码请求路径中的特殊字符
        path = path.encode('utf-8')
        path = urllib.parse.unquote(path)
        # 调用父类的方法，获取处理后的路径
        translated_path = super().translate_path(path)
        return translated_path


class Server(threading.Thread):
    def __init__(self, port: int, path: str = "shared") -> None:
        super().__init__()
        self.dir = path
        handler = partial(Utf8HTTPRequestHandler, directory=path)
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
