#!/usr/bin/env python
import sys
import socket


class KVClient(object):
    """ client for kv operation """
    def __init__(self, port=11211):
        self.host = "127.0.0.1"
        self.port = int(port)

    def set(self, key, value):
        """ kv set """
        self._estab_connect()
        self._set(key, value)

    def get(self, key):
        """ do not set value to 'None' """
        self._estab_connect()
        return self._get(key)

    def _set(self, key, value):
        key = str(key)
        size = len(str(value))
        value = str(value)
        msg = ''.join(["set ", key, " ", str(size), "\r\n", str(value)])
        self._send(msg)

    def _get(self, key):
        msg = ''.join(["get ", str(key), "\r\n"])
        val = self._send(msg)
        if val == "None":
            return None
        else:
            return val

    def _send(self, msg):
        self.sock.sendall(msg)
        # TODO: 处理变长数据
        return self.sock.recv(4096)

    def _estab_connect(self):
        """ establish a new socket connection """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


if __name__ == "__main__":
    port =11211 
    client = KVClient(port)
    client.set("key", "")
    print len(client.get("key"))
    print type(client.get("key"))
