#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
import asyncore
import socket


class HttpClient(object):

    def __init__(self, package):
        super(HttpClient, self).__init__()
        assert isinstance(package, HttpPackage)
        self._request_pack = package
        self._sock = socket.socket()
        self._response = ''

    def request(self):
        self._sock.connect(self._request_pack.host, self._request_pack.port)
        self._response = self._sock.send(self._request_pack)

    @property
    def response(self):
        return self._response

    def __del__(self):
        self._sock.close()
        super(HttpClient, self).__del__()


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


class Proxy(asyncore.dispatcher_with_send):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            package = sock.recv(8192)
            print package
            p_sock = socket.socket()
            p_sock.connect(('www.baidu.com', 443))
            p_sock.send(package)
            res = p_sock.recv()
            print res
            p_sock.close()
            sock.send(res)

    def handle_read(self):
        package = self.recv(8192)
        self.log_info(package)

proxy = Proxy('localhost', 1234)
asyncore.loop()
