# partiell

Partial argument application using `...`.

## Description

An enhanced version of [`functools.partial()`](
https://docs.python.org/3/library/functools.html#functools.partial) that
allows partially applying positional arguments from both the left and right
sides of the argument list.

We use `...` (the _Ellipsis_ object) as a placeholder in the argument list for
the arguments that are **not** yet supplied. The object returned from `partial()`
also supports being called with `...` for further partial application.

Use `partial` as a function decorator (`@partial`) to make a function
automatically support partial argument application with `...`.

## Usage

As a drop-in replacement for `functools.partial()`:

```python
>>> from partiell import partial
>>> from operator import mul, truediv

>>> double = partial(mul, 2)  # same as functools.partial()
>>> double(5)
10

>>> halve = partial(truediv, ..., 2)  # functools.partial() cannot do this
>>> halve(3)
1.5
```

As a function decorator to enable smoother partial function application:

```python
>>> @partial
... def f(x, y, z):
...    return x * 100 + y * 10 + z
```

`f()` can now be called with `...` for partial function application:

```python
>>> g = f(1, ...)  # Supply first argument only (x)
>>> g(2, 3)  # Supply the two remaining arguments (y, z)
123
```

Functions derived from `f()` automatically support `...` themselves:

```python
>>> h = g(2, ...)  # Supply g's first argument (y)
>>> h(3)  # Supply the final argument (z)
123
```

Using the `...` placeholder also allows supplying arguments right-to-left:

```python
>>> i = f(..., 3)  # Supply last argument only (z)
>>> i(1, 2)  # Supply the remaining arguments (x, y)
123
```

We can even supply arguments from both ends simultaneously:

```python
>>> j = f(1, ..., 3)  # Supply first and last argument (x, z)
>>> j(2)  # Supply the remaining argument (y)
123
```

## Discussion

Using `...` as a placeholder for future function arguments allows for a
"functional light" programming style that is somewhere between the verbosity
of invoking partial() explicitly and the implicit currying provided by e.g.
the `@curry` decorator in [PyMonad](https://pypi.org/project/PyMonad/).

The idea of using `...` as a placeholder for function arguments and having it
convert a function call into a partial function application is not new.
AFAICS, it was first discussed on [python-list in 2005](
https://www.mail-archive.com/python-list@python.org/msg17922.html), around the
time `partial()` was first added to the Python standard library ([PEP 309](
https://www.python.org/dev/peps/pep-0309/)).

## Installation

Run the following to install:

```bash
$ pip install partiell
```

## Development

To work on partiell, clone [this repo](https://github.com/jherland/partiell/),
and run the following (in a virtualenv) to get everything you need to develop
and run tests:

```bash
$ pip install -e .[dev]
```

Alternatively, if you are using Nix, simply use the bundled `shell.nix` to get
a development environment:

```bash
$ nix-shell
```

Use `nox` to run all tests (as defined in `noxfile.py`):

```bash
$ nox
```

## Contributing

Main development happens at <https://github.com/jherland/partiell/>.
Post issues and PRs there.
