#!/usr/bin/python
class InvalidMethod(Exception):
    """ Raised when the request method is not allowed by the View. """


class View(object):
    """ Blatantly modeled after Django's generic View. """
    allowed_methods = ['get', 'put', 'post', 'delete']

    def __init__(self, request):
        self.request = request

    def __call__(self):
        return self.dispatch()

    def dispatch(self):
        if self.request.method in map(str.upper, self.allowed_methods):
            method = getattr(self, self.request.method.lower())
            return method()
        else:
            # Method not allowed, raise error
            raise InvalidMethod(str(self.request.method))

    def get(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()

    def post(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()
