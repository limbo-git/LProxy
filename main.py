#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'limbo'

"""
"""
import asyncore
import socket

BUFFER_SIZE = 8192

send_queue = []
echo_queue = []


class HttpClient(asyncore.dispatcher):

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

    def writable(self):
        global send_queue
        return True if send_queue else False

    def handle_connect(self):
        self.log_info('httpclient connect')
        self.send('GET / HTTP/1.0\r\n\r\n')

    def handle_read(self):
        global echo_queue
        echo_queue.append(self.recv(BUFFER_SIZE))

    def handle_write(self):
        global send_queue
        self.send(send_queue.pop(0))


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


class ProxyHandle(asyncore.dispatcher):

    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        self.client = HttpClient()

    def writable(self):
        global echo_queue
        return True if echo_queue else False

    def handle_read(self):
        global send_queue
        print 'ProxyHandle'
        data = self.recv(BUFFER_SIZE)
        self.log_info(data)
        if not self.client.connected:
            self.client.connect(('www.python.org', 80))

    def handle_write(self):
        global echo_queue
        self.send(echo_queue.pop(0))


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
            self.handles.append(ProxyHandle(sock))
            # todo: put accept socket into another map

    def handle_read(self):
        package = self.recv(BUFFER_SIZE)
        self.log_info(package)


def test():
    Proxy('localhost', 1234)
    asyncore.loop()

if __name__ == '__main__':
    test()
