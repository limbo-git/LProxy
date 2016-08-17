#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'limbo'

"""
"""
import asyncore
import socket

from errno import EAGAIN

from http import AsyncHttpClient as HttpClient
from http.parser import HttpParser


class ProxyHandle(asyncore.dispatcher_with_send):

    def __init__(self, sock, map=None):
        asyncore.dispatcher_with_send.__init__(self, sock, map)

    def handle_read(self):
        self.log_info('ProxyHandle->read')

    def handle_write(self):
        self.log_info('ProxyHandle->write')


class HttpProxyHandle(ProxyHandle):

    def __init__(self, sock):
        ProxyHandle.__init__(self, sock)
        self.request_queue, self.response_queue = [], []
        # self.client = HttpClient(self.request_queue, self.response_queue)
        self.parser = HttpParser()

    def writable(self):
        return True if self.response_queue else False

    def handle_read(self):
        ProxyHandle.handle_read(self)
        data = ''
        while True:
            try:
                data += self.recv(1)
            except socket.error as e:
                break
        print data
        # if not self.client.connected:
        # self.client.connect(('www.baidu.com', 443))
        # self.request_queue.append(data)

    def handle_write(self):
        ProxyHandle.handle_write(self)
        while len(self.response_queue) > 0:
            self.send(self.response_queue.pop(0))


class Proxy(asyncore.dispatcher_with_send):

    def __init__(self, host, port):
        asyncore.dispatcher_with_send.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(1)
        self.handles = []

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.handles.append(HttpProxyHandle(sock))
            # todo: put accept socket into another map

    def handle_read(self):
        package = self.recv(BUFFER_SIZE)
        self.log_info(package)


def test():
    Proxy('localhost', 1234)
    asyncore.loop()

if __name__ == '__main__':
    test()
