import functools
import time
import warnings
import traceback

__all__ = ["none", "attempt_retries", "ignore_exception",
           "asynchronous", "timer", "abstract", "synchronized",
           "count_calls", "memoized", "deprecated", "time_out",
           "attempt_retries_details"]


def none(func):
    """
    Null decorator that does absolutely nothing
    Useful for overriding other decorators in mock testing
    """
    return func


def attempt_retries(func, retries=3, delay=0.3, IgnoreException=Exception):
    """
    Decorator for ignoring certain exception for certain number times and
    retrying with certain delay
    e.g.   func = @retry(connect_imap, 10, 5, SocketError)
    e.g.2. retry(connect_imap)(username, password)
    @returns the original function with an external retry wrapper
    """
    def dec(*args, **kwargs):
        for i in range(retries-1):
            try:
                return func(*args, **kwargs)
            except IgnoreException:
                time.sleep(delay)
        out = func(*args, **kwargs)
    return dec

# capture err details


def attempt_retries_detailed(func, retries=3,
                             delay=0.3, IgnoreException=Exception):
    """
    Decorator for ignoring certain exception for certain number
    times and retrying with certain delay
    e.g.   func = @retry(connect_imap, 10, 5, SocketError) # Tries ten times
    e.g.2. retry(connect_imap)(username, password)
    @returns the original function with an external retry wrapper
    """
    def dec(*args, **kwargs):
        for i in range(retries-1):
            try:
                return func(*args, **kwargs)
            except IgnoreException:
                time.sleep(delay)
        try:
            out = func(*args, **kwargs)
        except Exception as e:
            err = traceback.format_exc()
            err += "%s\n" % e.__class__
            if args:
                err += "\tArgs: (%s)\n" % str(args[:10])
            if kwargs:
                err += "\tKwargs: (%s)" % str(kwargs.items()[:10])
            raise Exception(err)
    return dec


def ignore_exception(func):
    """
    Decorator for supressing all exceptions
    """
    def dec(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            pass
    return dec


def abstract(func):
    """
    Mark function as abstract.
    Function will raise exception unless it is overridden in subclass
    """
    def dec(*args, **kwds):
        raise Exception(
            "Abstract function %s() must be overridden" % func.__name__)
    return dec


def synchronized(lock):
    """ Synchronization decorator """
    def wrap(f):
        def dec(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return dec
    return wrap


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.
    """
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


class memoized(object):
    """
    Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


def cache(func):
    """Keep a cache of previous function calls"""
    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_cache.cache:
            wrapper_cache.cache[cache_key] = func(*args, **kwargs)
        return wrapper_cache.cache[cache_key]
    wrapper_cache.cache = dict()
    return wrapper_cache


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


def auto_invoked_fn(func):
    """Self executing function"""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        func(*args, **kwargs)
    return inner()