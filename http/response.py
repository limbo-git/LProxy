# -*- coding: utf-8 -*-
# __author__ = 'limbo'


class Response(object):
    """docstring for Response"""

    def __init__(self, data):
        super(Response, self).__init__()
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass
