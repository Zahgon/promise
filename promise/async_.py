# Based on https://github.com/petkaantonov/bluebird/blob/master/src/promise.js
from collections import deque
from threading import local

if False:
    from .promise import Promise
    from typing import Any, Callable, Optional, Union  # flake8: noqa


class Async(local):
    def __init__(self, trampoline_enabled=True):
        self.is_tick_used = False
        self.late_queue = deque()  # type: ignore
        self.normal_queue = deque()  # type: ignore
        self.have_drained_queues = False
        self.trampoline_enabled = trampoline_enabled

    def enable_trampoline(self):
        pass

    def disable_trampoline(self):
        pass

    def have_items_queued(self):
        pass

    def _async_invoke_later(self, fn, scheduler):
        pass

    def _async_invoke(self, fn, scheduler):
        # type: (Callable, Any) -> None
        pass

    def _async_settle_promise(self, promise):
        # type: (Promise) -> None
        pass

    def invoke_later(self, fn):
        pass

    def invoke(self, fn, scheduler):
        # type: (Callable, Any) -> None
        pass

    def settle_promises(self, promise):
        # type: (Promise) -> None
        pass

    def throw_later(self, reason, scheduler):
        # type: (Exception, Any) -> None
        pass

    fatal_error = throw_later

    def drain_queue(self, queue):
        # type: (deque) -> None
        pass

    def drain_queue_until_resolved(self, promise):
        # type: (Promise) -> None
        pass

    def wait(self, promise, timeout=None):
        # type: (Promise, Optional[float]) -> None
        pass

    def drain_queues(self):
        # type: () -> None
        pass

    def queue_tick(self, scheduler):
        # type: (Any) -> None
        pass

    def reset(self):
        # type: () -> None
        pass
