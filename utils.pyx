import cython
import numpy as np
cimport numpy as cnp
ctypedef cnp.int_t DTYPE_t


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cnp.ndarray[DTYPE_t] _transform(cnp.ndarray[DTYPE_t] arr):
    cdef:
        int i = 0
        int n = arr.shape[0]
        int x
        cnp.ndarray[DTYPE_t] new_arr = np.empty_like(arr)

    while i < n:
        x = arr[i]
        if x % 2:
            new_arr[i] = x + 1
        else:
            new_arr[i] = x - 1
        i += 1
    return new_arr
