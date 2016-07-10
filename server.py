#! /usr/bin/env python
#-*- encoding:utf-8 -*-
""" simple kv store"""
import socket
import threading
import sys


CACHE = {}

def handle_con(conn):
    """ connection handler """
    sockfile = conn.makefile(mode="rw")
    while True:
        line = sockfile.readline()
        if line == "":
            conn.close()
            break
        parts = line.split()
        cmd = parts[0]
        if cmd == "get":
            key = parts[1]
            val = CACHE.get(key)
            if val is None:
                output(sockfile, None)
            else:
                output(sockfile, val)
        elif cmd == "set":
            key = parts[1]
            length = int(parts[2])
            val = sockfile.read(length)[:length]
            print key, val
            CACHE[key] = val

            output(sockfile, "STORED\r\n")
        sockfile.flush()


def output(sockfile, string):
    """ actually write to socket """
    sockfile.write(string)


class KVInfo(object):
    """ simple kv info """
    def __init__(self, kv_port=11211):
        self.kv_port = kv_port


class KVStore(object):
    """ simple kv store """
    def __init__(self, port=11211):
        self.port = port

    def serve(self):
        """ running synchronously """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", self.port))
        self.sock.listen(1)

        while(1):
            conn, _ = self.sock.accept()
            thread = threading.Thread(target=handle_con, args=(conn,))
            thread.start()

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


if __name__ == "__main__":
    port = sys.argv[1]
    kv = KVStore(int(port))
    kv.serve()

