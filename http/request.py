# -*- coding: utf-8 -*-
# __author__ = 'limbo'


class Request(object):
    """docstring for Request"""

    def __init__(self, data):
        super(Request, self).__init__()
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
