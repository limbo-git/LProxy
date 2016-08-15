#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
import asyncore
import socket

RECV_SOCK_MAP = {}
SEND_SOCK_MAP = {}


class AsyncHttpClient(asyncore.dispatcher):

    def __init__(self):
        asyncore.dispatcher.__init__()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = None

    def handle_read(self):
        print self.recv(8192)

    def writeable(self):
        return True if buffer else False

    def handle_write(self):
        self.send(self[:1024])
        self.buffer = self.buffer[1024:]


class HttpPackage(object):

    def __init__(self, data):
        super(HttpPackage, self).__init__()
        self._data = data

    @property
    def host(self):
        pass

    @property
    def port(self):
        return self._port


class ProxyHandle(asyncore.dispatcher_with_send):

    def handle_read(self):
        print 'ProxyHandle'
        print self.recv(8192)

    def handle_write(self):
        pass


class Proxy(asyncore.dispatcher_with_send):

    def __init__(self, host, port):
        asyncore.dispatcher_with_send.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            ProxyHandle(sock)
            # todo: put accept socket into another map

    def handle_read(self):
        package = self.recv(8192)
        self.log_info(package)

proxy = Proxy('localhost', 1234)
asyncore.loop()
