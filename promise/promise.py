from collections import namedtuple
from functools import partial, wraps
from sys import version_info, exc_info
from threading import RLock
from types import TracebackType
from weakref import WeakKeyDictionary

from six import reraise  # type: ignore
from .async_ import Async
from .compat import (
    Future,
    ensure_future,
    iscoroutine,  # type: ignore
    iterate_promise,
)  # type: ignore
from .utils import deprecated, integer_types, string_types, text_type, binary_type, warn
from .promise_list import PromiseList
from .schedulers.immediate import ImmediateScheduler
from typing import TypeVar, Generic

# from .schedulers.gevent import GeventScheduler
# from .schedulers.asyncio import AsyncioScheduler
# from .schedulers.thread import ThreadScheduler

if False:
    from typing import (
        Type,
        List,
        Any,
        Callable,
        Dict,
        Iterator,
        Optional,  # flake8: noqa
        Tuple,
        Union,
        Generic,
        Hashable,
        MutableMapping,
    )


default_scheduler = ImmediateScheduler()

async_instance = Async()


def get_default_scheduler():
    # type: () -> ImmediateScheduler
    pass


def set_default_scheduler(scheduler):
    pass


IS_PYTHON2 = version_info[0] == 2
DEFAULT_TIMEOUT = None  # type: Optional[float]

MAX_LENGTH = 0xFFFF | 0
CALLBACK_SIZE = 3

CALLBACK_FULFILL_OFFSET = 0
CALLBACK_REJECT_OFFSET = 1
CALLBACK_PROMISE_OFFSET = 2

BASE_TYPES = set(
    integer_types
    + string_types
    + (bool, float, complex, tuple, list, dict, text_type, binary_type)
)

# These are the potential states of a promise
STATE_PENDING = -1
STATE_REJECTED = 0
STATE_FULFILLED = 1


def make_self_resolution_error():
    # type: () -> TypeError
    pass


def try_catch(handler, *args, **kwargs):
    # type: (Callable, Any, Any) -> Union[Tuple[Any, None], Tuple[None, Tuple[Exception, Optional[TracebackType]]]]
    pass


T = TypeVar("T")
S = TypeVar("S", contravariant=True)


class Promise(Generic[T]):
    """
    This is the Promise class that complies
    Promises/A+ specification.
    """

    # __slots__ = ('_state', '_is_final', '_is_bound', '_is_following', '_is_async_guaranteed',
    #              '_length', '_handlers', '_fulfillment_handler0', '_rejection_handler0', '_promise0',
    #              '_is_waiting', '_future', '_trace', '_event_instance'
    #              )

    _state = STATE_PENDING  # type: int
    _is_final = False
    _is_bound = False
    _is_following = False
    _is_async_guaranteed = False
    _length = 0
    _handlers = None  # type: Dict[int, Union[Callable, Promise, None]]
    _fulfillment_handler0 = None  # type: Any
    _rejection_handler0 = None  # type: Any
    _promise0 = None  # type: Optional[Promise]
    _future = None  # type: Future
    _traceback = None  # type: Optional[TracebackType]
    # _trace = None
    _is_waiting = False
    _scheduler = None

    def __init__(self, executor=None, scheduler=None):
        # type: (Optional[Callable[[Callable[[T], None], Callable[[Exception], None]], None]], Any) -> None
        """
        Initialize the Promise into a pending state.
        """
        # self._state = STATE_PENDING  # type: int
        # self._is_final = False
        # self._is_bound = False
        # self._is_following = False
        # self._is_async_guaranteed = False
        # self._length = 0
        # self._handlers = None  # type: Dict[int, Union[Callable, None]]
        # self._fulfillment_handler0 = None  # type: Union[Callable, partial]
        # self._rejection_handler0 = None  # type: Union[Callable, partial]
        # self._promise0 = None  # type: Promise
        # self._future = None  # type: Future
        # self._event_instance = None # type: Event

        # self._is_waiting = False
        self._scheduler = scheduler

        if executor is not None:
            self._resolve_from_executor(executor)

        # For compatibility reasons
        # self.reject = self._deprecated_reject
        # self.resolve = self._deprecated_resolve

    @property
    def scheduler(self):
        # type: () -> ImmediateScheduler
        pass

    @property
    def future(self):
        # type: (Promise) -> Future
        pass

    def __iter__(self):
        # type: () -> Iterator
        return iterate_promise(self._target())  # type: ignore

    __await__ = __iter__

    @deprecated(
        "Rejecting directly in a Promise instance is deprecated, as Promise.reject() is now a class method. "
        "Please use promise.do_reject() instead.",
        name="reject",
    )
    def _deprecated_reject(self, e):
        pass

    @deprecated(
        "Resolving directly in a Promise instance is deprecated, as Promise.resolve() is now a class method. "
        "Please use promise.do_resolve() instead.",
        name="resolve",
    )
    def _deprecated_resolve(self, value):
        pass

    def _resolve_callback(self, value):
        # type: (T) -> None
        pass

    def _settled_value(self, _raise=False):
        # type: (bool) -> Any
        pass

    def _fulfill(self, value):
        # type: (T) -> None
        pass

    def _reject(self, reason, traceback=None):
        # type: (Exception, Optional[TracebackType]) -> None
        pass

    def _ensure_possible_rejection_handled(self):
        # type: () -> None
        # self._rejection_is_unhandled = True
        # async_instance.invoke_later(self._notify_unhandled_rejection, self)
        pass

    def _reject_callback(self, reason, synchronous=False, traceback=None):
        # type: (Exception, bool, Optional[TracebackType]) -> None
        pass

    def _clear_callback_data_index_at(self, index):
        # type: (int) -> None
        pass

    def _fulfill_promises(self, length, value):
        # type: (int, T) -> None
        pass

    def _reject_promises(self, length, reason):
        # type: (int, Exception) -> None
        pass

    def _settle_promise(
        self,
        promise,  # type: Optional[Promise]
        handler,  # type: Optional[Callable]
        value,  # type: Union[T, Exception]
        traceback,  # type: Optional[TracebackType]
    ):
        # type: (...) -> None
        pass

    def _settle_promise0(
        self,
        handler,  # type: Optional[Callable]
        value,  # type: Any
        traceback,  # type: Optional[TracebackType]
    ):
        # type: (...) -> None
        pass

    def _settle_promise_from_handler(self, handler, value, promise):
        # type: (Callable, Any, Promise) -> None
        pass

    def _promise_at(self, index):
        # type: (int) -> Optional[Promise]
        pass

    def _fulfillment_handler_at(self, index):
        # type: (int) -> Optional[Callable]
        pass

    def _rejection_handler_at(self, index):
        # type: (int) -> Optional[Callable]
        pass

    def _migrate_callback0(self, follower):
        # type: (Promise) -> None
        pass

    def _migrate_callback_at(self, follower, index):
        pass

    def _add_callbacks(
        self,
        fulfill,  # type: Optional[Callable]
        reject,  # type: Optional[Callable]
        promise,  # type: Optional[Promise]
    ):
        # type: (...) -> int
        pass

    def _target(self):
        # type: () -> Promise
        pass

    def _followee(self):
        # type: () -> Promise
        pass

    def _set_followee(self, promise):
        # type: (Promise) -> None
        pass

    def _settle_promises(self):
        # type: () -> None
        pass

    def _resolve_from_executor(self, executor):
        # type: (Callable[[Callable[[T], None], Callable[[Exception], None]], None]) -> None
        # self._capture_stacktrace()
        pass

    @classmethod
    def wait(cls, promise, timeout=None):
        # type: (Promise, Optional[float]) -> None
        pass

    def _wait(self, timeout=None):
        # type: (Optional[float]) -> None
        pass

    def get(self, timeout=None):
        # type: (Optional[float]) -> T
        pass

    def _target_settled_value(self, _raise=False):
        # type: (bool) -> Any
        pass

    _value = _reason = _target_settled_value
    value = reason = property(_target_settled_value)

    def __repr__(self):
        # type: () -> str
        hex_id = hex(id(self))
        if self._is_following:
            return "<Promise at {} following {}>".format(hex_id, self._target())
        state = self._state
        if state == STATE_PENDING:
            return "<Promise at {} pending>".format(hex_id)
        elif state == STATE_FULFILLED:
            return "<Promise at {} fulfilled with {}>".format(
                hex_id, repr(self._rejection_handler0)
            )
        elif state == STATE_REJECTED:
            return "<Promise at {} rejected with {}>".format(
                hex_id, repr(self._fulfillment_handler0)
            )

        return "<Promise unknown>"

    @property
    def is_pending(self):
        # type: (Promise) -> bool
        """Indicate whether the Promise is still pending. Could be wrong the moment the function returns."""
        pass

    @property
    def is_fulfilled(self):
        # type: (Promise) -> bool
        """Indicate whether the Promise has been fulfilled. Could be wrong the moment the function returns."""
        pass

    @property
    def is_rejected(self):
        # type: (Promise) -> bool
        """Indicate whether the Promise has been rejected. Could be wrong the moment the function returns."""
        pass

    def catch(self, on_rejection):
        # type: (Promise, Callable[[Exception], Any]) -> Promise
        """
        This method returns a Promise and deals with rejected cases only.
        It behaves the same as calling Promise.then(None, on_rejection).
        """
        pass

    def _then(
        self,
        did_fulfill=None,  # type: Optional[Callable[[T], S]]
        did_reject=None,  # type: Optional[Callable[[Exception], S]]
    ):
        # type: (...) -> Promise[S]
        pass

    fulfill = _resolve_callback
    do_resolve = _resolve_callback
    do_reject = _reject_callback

    def then(self, did_fulfill=None, did_reject=None):
        # type: (Promise, Callable[[T], S], Optional[Callable[[Exception], S]]) -> Promise[S]
        """
        This method takes two optional arguments.  The first argument
        is used if the "self promise" is fulfilled and the other is
        used if the "self promise" is rejected.  In either case, this
        method returns another promise that effectively represents
        the result of either the first of the second argument (in the
        case that the "self promise" is fulfilled or rejected,
        respectively).
        Each argument can be either:
          * None - Meaning no action is taken
          * A function - which will be called with either the value
            of the "self promise" or the reason for rejection of
            the "self promise".  The function may return:
            * A value - which will be used to fulfill the promise
              returned by this method.
            * A promise - which, when fulfilled or rejected, will
              cascade its value or reason to the promise returned
              by this method.
          * A value - which will be assigned as either the value
            or the reason for the promise returned by this method
            when the "self promise" is either fulfilled or rejected,
            respectively.
        :type success: (Any) -> object
        :type failure: (Any) -> object
        :rtype : Promise
        """
        pass

    def done(self, did_fulfill=None, did_reject=None):
        # type: (Optional[Callable], Optional[Callable]) -> None
        pass

    def done_all(self, handlers=None):
        # type: (Promise, Optional[List[Union[Dict[str, Optional[Callable]], Tuple[Callable, Callable], Callable]]]) -> None
        """
        :type handlers: list[(Any) -> object] | list[((Any) -> object, (Any) -> object)]
        """
        pass

    def then_all(self, handlers=None):
        # type: (Promise, List[Callable]) -> List[Promise]
        """
        Utility function which calls 'then' for each handler provided. Handler can either
        be a function in which case it is used as success handler, or a tuple containing
        the success and the failure handler, where each of them could be None.
        :type handlers: list[(Any) -> object] | list[((Any) -> object, (Any) -> object)]
        :param handlers
        :rtype : list[Promise]
        """
        pass

    @classmethod
    def _try_convert_to_promise(cls, obj):
        # type: (Any) -> Promise
        pass

    @classmethod
    def reject(cls, reason):
        # type: (Exception) -> Promise
        pass

    rejected = reject

    @classmethod
    def resolve(cls, obj):
        # type: (T) -> Promise[T]
        pass

    cast = resolve
    fulfilled = cast

    @classmethod
    def promisify(cls, f):
        # type: (Callable) -> Callable[..., Promise]
        pass

    _safe_resolved_promise = None  # type: Promise

    @classmethod
    def safe(cls, fn):
        # type: (Callable) -> Callable
        pass

    @classmethod
    def all(cls, promises):
        # type: (Any) -> Promise
        pass

    @classmethod
    def for_dict(cls, m):
        # type: (Dict[Hashable, Promise[S]]) -> Promise[Dict[Hashable, S]]
        """
        A special function that takes a dictionary of promises
        and turns them into a promise for a dictionary of values.
        In other words, this turns an dictionary of promises for values
        into a promise for a dictionary of values.
        """
        pass

    @classmethod
    def is_thenable(cls, obj):
        # type: (Any) -> bool
        """
        A utility function to determine if the specified
        object is a promise using "duck typing".
        """
        pass


_type_done_callbacks = WeakKeyDictionary()  # type: MutableMapping[type, bool]


def is_future_like(_type):
    # type: (type) -> bool
    pass


promisify = Promise.promisify
promise_for_dict = Promise.for_dict
is_thenable = Promise.is_thenable


def _process_future_result(resolve, reject):
    # type: (Callable, Callable) -> Callable
    pass
