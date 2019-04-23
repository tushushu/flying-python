import pyximport
pyximport.install()

from _no_gil_lock import _add_one  # pylint: disable=import-error


def add_one(n_times=10 ** 7):
    return _add_one(n_times)
