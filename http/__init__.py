# -*- coding: utf-8 -*-
# __author__ = 'limbo'

import socket
import asyncore

from .parser import HttpParser
from errno import EAGAIN, EWOULDBLOCK


class AsyncHttpClient(asyncore.dispatcher):

    def __init__(self, request_queue, response_queue, h_parser=None):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.parser = h_parser if h_parser is not None else HttpParser()

    def writable(self):
        return True if self.request_queue else False

    def handle_connect(self):
        # self.request_queue.append('GET / HTTP/1.1\r\n\r\n')
        self.log_info('httpclient connect')

    def handle_read(self):
        self.log_info('HttpClient->read')
        temp = ''
        try:
            while True:
                try:
                    temp += self.recv(1)
                except:
                    import traceback
                    traceback.print_exc()
                    break
            print temp
            self.response_queue.append(temp)
            # while True:
            #     try:
            #         char = self.recv(1)
            #     except socket.error as e:
            #         if e.args[0] == EAGAIN:
            #             break
            #         elif e.args[0] == EWOULDBLOCK:
            #             break
            #         else:
            #             raise e
            #     response = self.parser.encode(char)
            # if response:
            #     self.response_queue.append(response)
        except:
            import traceback
            traceback.print_exc()

    def handle_write(self):
        self.log_info('HttpClient->write')
        while len(self.request_queue) > 0:
            self.send(self.request_queue.pop(0))


class SyncHttpClient(object):
    """docstring for SyncHttpClient"""

    def __init__(self):
        super(SyncHttpClient, self).__init__()
        self.parser = HttpParser()
