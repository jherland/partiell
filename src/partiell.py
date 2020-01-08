"""partiell.py - Partial argument application using '...'
"""
# Written by Nick Coghlan <ncoghlan at gmail.com>,
# Raymond Hettinger <python at rcn.com>,
# Łukasz Langa <lukasz at langa.pl>,
# and Johan Herland <johan at herland.net>.
#   Copyright (C) 2006-2019 Python Software Foundation.

__all__ = ["partial"]

from reprlib import recursive_repr


################################################################################
### partial() argument application
################################################################################

# Purely functional, no descriptor behaviour
class partial:
    """New function with partial application of the given arguments
    and keywords.

    An enhanced version of functools.partial() that allows partially applying
    positional arguments from both the left and right sides of the argument
    list.

    We use '...' (the Ellipsis object) as a placeholder in the argument list
    for the arguments that are not yet supplied. The object returned from here
    also supports being called with '...' for further partial application.

    Use as a function decorator (@partial) to make a function automatically
    support partial argument application with '...'.

    Usage:

    As a drop-in replacement for functools.partial():

    >>> from operator import mul, truediv
    >>> double = partial(mul, 2)  # same as functools.partial()
    >>> double(5)
    10
    >>> halve = partial(truediv, ..., 2)  # functools.partial() cannot do this
    >>> halve(3)
    1.5

    As a function decorator to enable smoother partial function application:

    >>> @partial
    ... def f(x, y, z):
    ...    return x * 100 + y * 10 + z

    f() can now be called with '...' for partial function application:

    >>> g = f(1, ...)  # Supply first argument only (x)
    >>> g(2, 3)  # Supply the two remaining arguments (y, z)
    123

    Functions derived from f() automatically support '...' themselves:

    >>> h = g(2, ...)  # Supply g's first argument (y)
    >>> h(3)  # Supply the final argument (z)
    123

    Using the '...' placeholder also allows supplying arguments right-to-left:

    >>> i = f(..., 3)  # Supply last argument only (z)
    >>> i(1, 2)  # Supply the remaining arguments (x, y)
    123

    We can even supply arguments from both ends simultaneously:

    >>> j = f(1, ..., 3)  # Supply first and last argument (x, z)
    >>> j(2)  # Supply the remaining argument (y)
    123
    """

    __slots__ = "func", "largs", "rargs", "keywords", "__dict__", "__weakref__"

    def __new__(cls, func, /, *args, **keywords):
        if not callable(func):
            raise TypeError("the first argument must be callable")

        # split args into left and right parts
        ellipsis = None
        for i, arg in enumerate(args):
            if arg is Ellipsis:
                if ellipsis is None:
                    ellipsis = i
                else:
                    raise TypeError("cannot use more than one ... in arguments")
        if ellipsis is None:  # same behavior as partial()
            largs = tuple(args)
            rargs = tuple()
        else:
            largs = tuple(args[:ellipsis])
            rargs = tuple(args[ellipsis + 1 :])

        if hasattr(func, "func"):
            largs = func.largs + largs
            rargs = rargs + func.rargs
            keywords = {**func.keywords, **keywords}
            func = func.func

        self = super(partial, cls).__new__(cls)

        self.func = func
        self.largs = largs
        self.rargs = rargs
        self.keywords = keywords
        return self

    def __call__(self, /, *args, **keywords):
        for arg in args:
            if arg is Ellipsis:  # another partial application
                return self.__new__(type(self), self, *args, **keywords)

        # final application
        keywords = {**self.keywords, **keywords}
        return self.func(*self.largs, *args, *self.rargs, **keywords)

    @recursive_repr()
    def __repr__(self):
        qualname = type(self).__qualname__
        args = [repr(self.func)]
        args.extend(repr(x) for x in self.largs)
        args.append("...")
        args.extend(repr(x) for x in self.rargs)
        args.extend(f"{k}={v!r}" for (k, v) in self.keywords.items())
        if type(self).__module__ == "partiell":
            return f"partiell.{qualname}({', '.join(args)})"
        return f"{qualname}({', '.join(args)})"

    def __reduce__(self):
        return (
            type(self),
            (self.func,),
            (
                self.func,
                self.largs,
                self.rargs,
                self.keywords or None,
                self.__dict__ or None,
            ),
        )

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError("argument to __setstate__ must be a tuple")
        if len(state) != 5:
            raise TypeError(f"expected 5 items in state, got {len(state)}")
        func, largs, rargs, kwds, namespace = state
        if (
            not callable(func)
            or not isinstance(largs, tuple)
            or not isinstance(rargs, tuple)
            or (kwds is not None and not isinstance(kwds, dict))
            or (namespace is not None and not isinstance(namespace, dict))
        ):
            raise TypeError("invalid partial state")

        largs = tuple(largs)  # just in case it's a subclass
        rargs = tuple(rargs)  # just in case it's a subclass
        if kwds is None:
            kwds = {}
        elif type(kwds) is not dict:  # XXX does it need to be *exactly* dict?
            kwds = dict(kwds)
        if namespace is None:
            namespace = {}

        self.__dict__ = namespace
        self.func = func
        self.largs = largs
        self.rargs = rargs
        self.keywords = kwds
