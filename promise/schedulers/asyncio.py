from __future__ import absolute_import

from asyncio import get_event_loop, Event


class AsyncioScheduler(object):
    def __init__(self, loop=None):
        self.loop = loop or get_event_loop()

    def call(self, fn):
        pass

    def wait(self, promise, timeout=None):
        pass
