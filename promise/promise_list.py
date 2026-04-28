from functools import partial
from types import TracebackType
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

if False:
    from .promise import Promise
    from typing import (
        Any,
        Optional,
        Tuple,
        Union,
        List,
        Type,
        Collection,
    )  # flake8: noqa


class PromiseList(object):

    __slots__ = ("_values", "_length", "_total_resolved", "promise", "_promise_class")

    def __init__(self, values, promise_class):
        # type: (Union[Collection, Promise[Collection]], Type[Promise]) -> None
        self._promise_class = promise_class
        self.promise = self._promise_class()

        self._length = 0
        self._total_resolved = 0
        self._values = None  # type: Optional[Collection]
        Promise = self._promise_class
        if Promise.is_thenable(values):
            values_as_promise = Promise._try_convert_to_promise(
                values
            )._target()  # type: ignore
            self._init_promise(values_as_promise)
        else:
            self._init(values)  # type: ignore

    def __len__(self):
        # type: () -> int
        return self._length

    def _init_promise(self, values):
        # type: (Promise[Collection]) -> None
        pass

    def _init(self, values):
        # type: (Collection) -> None
        pass

    def _iterate(self, values):
        # type: (Collection[Any]) -> None
        pass

    def _promise_fulfilled(self, value, i):
        # type: (Any, int) -> bool
        pass

    def _promise_rejected(self, reason, promise):
        # type: (Exception, Promise) -> bool
        pass

    @property
    def is_resolved(self):
        # type: () -> bool
        pass

    def _resolve(self, value):
        # type: (Collection[Any]) -> None
        pass

    def _reject(self, reason, traceback=None):
        # type: (Exception, Optional[TracebackType]) -> None
        pass
