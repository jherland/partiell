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
    """

    __slots__ = "func", "largs", "rargs", "keywords", "__dict__", "__weakref__"

    def __new__(cls, func, /, *args, **keywords):
        if not callable(func):
            raise TypeError("the first argument must be callable")

        largs = tuple(args)
        rargs = tuple()

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
        keywords = {**self.keywords, **keywords}
        return self.func(*self.largs, *args, *self.rargs, **keywords)

    @recursive_repr()
    def __repr__(self):
        qualname = type(self).__qualname__
        args = [repr(self.func)]
        args.extend(repr(x) for x in self.largs)
        args.extend(repr(x) for x in self.rargs)
        args.extend(f"{k}={v!r}" for (k, v) in self.keywords.items())
        if type(self).__module__ == "partiell":
            return f"partiell.{qualname}({', '.join(args)})"
        return f"{qualname}({', '.join(args)})"

    def __reduce__(self):
        return type(self), (self.func,), (self.func, self.largs, self.rargs,
               self.keywords or None, self.__dict__ or None)

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError("argument to __setstate__ must be a tuple")
        if len(state) != 5:
            raise TypeError(f"expected 5 items in state, got {len(state)}")
        func, largs, rargs, kwds, namespace = state
        if (not callable(func) or
           not isinstance(largs, tuple) or not isinstance(rargs, tuple) or
           (kwds is not None and not isinstance(kwds, dict)) or
           (namespace is not None and not isinstance(namespace, dict))):
            raise TypeError("invalid partial state")

        largs = tuple(largs)  # just in case it's a subclass
        rargs = tuple(rargs)  # just in case it's a subclass
        if kwds is None:
            kwds = {}
        elif type(kwds) is not dict: # XXX does it need to be *exactly* dict?
            kwds = dict(kwds)
        if namespace is None:
            namespace = {}

        self.__dict__ = namespace
        self.func = func
        self.largs = largs
        self.rargs = rargs
        self.keywords = kwds
