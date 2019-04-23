
def _add_one(long n_times= 10 ** 7):
    cdef long ret = 0
    with nogil:
        while ret < n_times:
            ret += 1
    return ret

