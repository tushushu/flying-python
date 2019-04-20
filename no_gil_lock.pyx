cdef long _add_one(long n_times= 10 ** 7):
    with nogil:
        long ret = 0
        while ret < n_times:
            ret += 1
    return ret

