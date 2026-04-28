from __future__ import absolute_import

from gevent.event import Event  # type: ignore
import gevent  # type: ignore


class GeventScheduler(object):
    def call(self, fn):
        # print fn
        pass

    def wait(self, promise, timeout=None):
        pass
