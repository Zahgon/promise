from threading import Event

if False:
    from ..promise import Promise
    from typing import Callable, Any, Optional  # flake8: noqa


class ImmediateScheduler(object):
    def call(self, fn):
        # type: (Callable) -> None
        pass

    def wait(self, promise, timeout=None):
        # type: (Promise, Optional[float]) -> None
        pass
