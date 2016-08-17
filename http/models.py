# -*- coding: utf-8 -*-
# __author__ = 'limbo'

import cStringIO
import weakref

STATUS_LINE = 'status_line'
HEADER = 'header'
BODY = 'body'


class Content(object):
    """docstring for Content"""

    def __init__(self):
        super(Content, self).__init__()
        self._weakdict = weakref.WeakKeyDictionary()
        self.data = cStringIO.StringIO()

    def __get__(self, instance, owner):
        return self._weakdict.get(instance, None)

    def __set__(self, instance, value):
        self._weakdict[instance] = value


class StatusLine(Content):
    """docstring for StatusLine"""

    def __init__(self):
        super(StatusLine, self).__init__()

    def parser(self):
        raise NotImplementedError()


class RequestStatusLine(StatusLine):

    def __init(self):
        super(RequestStatusLine, self).__init__()
        self.method = ''
        self.url = ''
        self.version = ''

    def parser(self):
        pass


class ResponseStatusLine(StatusLine):

    def __init(self):
        super(ResponseStatusLine, self).__init__()
        self.version = ''
        self.status = ''
        self.reason-phrase = ''

    def parser(self):
        pass


class Header(Content):

    def __init__(self):
        super(Header, self).__init__()

    def parser(self):
        raise NotImplementedError()


class RequestHeader(Header):
    """docstring for RequestHeader"""

    def __init__(self):
        super(RequestHeader, self).__init__()


class ResponseHeader(Header):
    """docstring for ResponseHeader"""

    def __init__(self):
        super(ResponseHeader, self).__init__()


class Body(Content):

    def __init__(self):
        super(Body, self).__init__()


class Request(object):
    """docstring for Request"""

    status_line = RequestStatusLine()
    header = RequestHeader()
    body = Body()

    def __init__(self):
        super(Request, self).__init__()


class Response(object):
    """docstring for Response"""

    status_line = ResponseStatusLine()
    header = ResponseHeader()
    body = Body()

    def __init__(self):
        super(Response, self).__init__()
