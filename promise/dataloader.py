from collections import namedtuple
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
from functools import partial
from threading import local

from .promise import Promise, async_instance, get_default_scheduler

if False:
    from typing import (
        Any,
        List,
        Sized,
        Callable,
        Optional,
        Tuple,
        Union,
        Iterator,
        Hashable,
    )  # flake8: noqa


def get_chunks(iterable_obj, chunk_size=1):
    # type: (List[Loader], int) -> Iterator
    pass


Loader = namedtuple("Loader", "key,resolve,reject")


class DataLoader(local):

    batch = True
    max_batch_size = None  # type: int
    cache = True

    def __init__(
        self,
        batch_load_fn=None,  # type: Callable
        batch=None,  # type: Optional[Any]
        max_batch_size=None,  # type: Optional[int]
        cache=None,  # type: Optional[Any]
        get_cache_key=None,  # type: Optional[Any]
        cache_map=None,  # type: Optional[Any]
        scheduler=None,  # type: Optional[Any]
    ):
        # type: (...) -> None

        if batch_load_fn is not None:
            self.batch_load_fn = batch_load_fn

        if not callable(self.batch_load_fn):
            raise TypeError(
                (
                    "DataLoader must be have a batch_load_fn which accepts "
                    "List<key> and returns Promise<List<value>>, but got: {}."
                ).format(batch_load_fn)
            )

        if batch is not None:
            self.batch = batch

        if max_batch_size is not None:
            self.max_batch_size = max_batch_size

        if cache is not None:
            self.cache = cache

        self.get_cache_key = get_cache_key or (lambda x: x)
        self._promise_cache = cache_map or {}
        self._queue = []  # type: List[Loader]
        self._scheduler = scheduler

    def load(self, key=None):
        # type: (Hashable) -> Promise
        """
        Loads a key, returning a `Promise` for the value represented by that key.
        """
        pass

    def do_resolve_reject(self, key, resolve, reject):
        # type: (Hashable, Callable, Callable) -> None
        # Enqueue this Promise to be dispatched.
        pass

    def load_many(self, keys):
        # type: (Iterable[Hashable]) -> Promise
        """
        Loads multiple keys, promising an array of values

        >>> a, b = await my_loader.load_many([ 'a', 'b' ])

        This is equivalent to the more verbose:

        >>> a, b = await Promise.all([
        >>>    my_loader.load('a'),
        >>>    my_loader.load('b')
        >>> ])
        """
        pass

    def clear(self, key):
        # type: (Hashable) -> DataLoader
        """
        Clears the value at `key` from the cache, if it exists. Returns itself for
        method chaining.
        """
        pass

    def clear_all(self):
        # type: () -> DataLoader
        """
        Clears the entire cache. To be used when some event results in unknown
        invalidations across this particular `DataLoader`. Returns itself for
        method chaining.
        """
        pass

    def prime(self, key, value):
        # type: (Hashable, Any) -> DataLoader
        """
        Adds the provied key and value to the cache. If the key already exists, no
        change is made. Returns itself for method chaining.
        """
        pass


# Private: Enqueue a Job to be executed after all "PromiseJobs" Jobs.
#
# ES6 JavaScript uses the concepts Job and JobQueue to schedule work to occur
# after the current execution context has completed:
# http://www.ecma-international.org/ecma-262/6.0/#sec-jobs-and-job-queues
#
# Node.js uses the `process.nextTick` mechanism to implement the concept of a
# Job, maintaining a global FIFO JobQueue for all Jobs, which is flushed after
# the current call stack ends.
#
# When calling `then` on a Promise, it enqueues a Job on a specific
# "PromiseJobs" JobQueue which is flushed in Node as a single Job on the
# global JobQueue.
#
# DataLoader batches all loads which occur in a single frame of execution, but
# should include in the batch all loads which occur during the flushing of the
# "PromiseJobs" JobQueue after that same execution frame.
#
# In order to avoid the DataLoader dispatch Job occuring before "PromiseJobs",
# A Promise Job is created with the sole purpose of enqueuing a global Job,
# ensuring that it always occurs after "PromiseJobs" ends.

# Private: cached resolved Promise instance
cache = local()

def enqueue_post_promise_job(fn, scheduler):
    # type: (Callable, Any) -> None
    pass


def dispatch_queue(loader):
    # type: (DataLoader) -> None
    """
    Given the current state of a Loader instance, perform a batch load
    from its current queue.
    """
    pass


def dispatch_queue_batch(loader, queue):
    # type: (DataLoader, List[Loader]) -> None
    # Collect all keys to be loaded in this dispatch
    pass


def failed_dispatch(loader, queue, error):
    # type: (DataLoader, Iterable[Loader], Exception) -> None
    """
    Do not cache individual loads if the entire batch dispatch fails,
    but still reject each request so they do not hang.
    """
    pass
