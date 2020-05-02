import logging

_LOG = logging.getLogger(__name__)


def tokenize(s):
    return [t.strip() for t in s.split()]


class Stack(object):
    def __init__(self):
        self.data = []

    def is_empty(self):
        return True if len(self.data) == 0 \
            else False

    def top(self):
        if self.is_empty():
            _LOG.debug('Stack is Empty')
            return 0
        else:
            return self.data[-1]

    def push(self, item):
        _LOG.debug('Pushing: %s', item)
        self.data.append(item)

    def pop(self):
        if not self.is_empty():
            _LOG.debug('popping: %s', self.top())
            return self.data.pop()
        else:
            _LOG.debug('Stack is Empty')
        return None
