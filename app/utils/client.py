from http.client import HTTPConnection
from bs4 import BeautifulSoup
import os


class Client:
    def __init__(self, host, port):
        self._conn = HTTPConnection(host, port, timeout=1)
        self._data = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def _get_resp(self, path):
        self._conn.request('GET', path)
        resp = self._conn.getresponse()
        payload = None
        if resp.status == 200:
            if (path[-1] == '/'):
                payload = resp.read().decode('utf-8')
            else:
                payload = resp.read()
        return resp.status, payload

    def _parse(self, html: str):
        soup = BeautifulSoup(html, 'lxml')
        for li in soup.ul.children:
            if (li.name == 'li'):
                name, href = str(li.a.string), str(li.a['href'])
                self._data.append((name, href))

    def get_folder(self, path: str = "/"):
        status, html = self._get_resp(path)
        self._data.clear()
        if status == 200:
            self._parse(html)
        else:
            print('error')
        return self._data

    def get_file(self, path):
        status, buf = self._get_resp(path)
        if (status != 200):
            print('error')
            return ''
        save_dir = "downloaded"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_path = os.path.join(save_dir, path.split('/')[-1])
        with open(save_path.encode('utf-8'), 'wb') as f:
            f.write(buf)
        return save_path

    def current_dir(self):
        return self._data


if __name__ == '__main__':
    with Client('localhost', 8888) as client:
        data = client.get_folder('/')
        print(*data)
        data = client.get_folder(data[1][1])
        print(*data)
