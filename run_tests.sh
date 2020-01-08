#!/bin/sh

set -e

python -m black .
python -m doctest src/*.py
python -m unittest discover
