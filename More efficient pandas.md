# 让Pandas DataFrame性能提升40倍

## 1. 小试牛刀
大名鼎鼎的Pandas是数据分析的神器。有时候我们需要对上千万甚至上亿的数据进行非常复杂处理，那么运行效率就是一个不能忽视的问题。比如下面这个简单例子，我们随机生成100万条数据，对'val'这一列进行处理：如果是偶数则减1，奇数则加1。实际的数据分析工作要比这个例子复杂的多，但考虑到我们（主要是我）没有那么多时间等待运行结果，所以就偷个懒吧。可以看到transform函数的平均运行时间是284ms，


```python
import pandas as pd
import numpy as np

def gen_data(size):
    d = dict()
    d["genre"] = np.random.choice(["A", "B", "C", "D"], size=size)
    d["val"] = np.random.randint(low=0, high=100, size=size)
    return pd.DataFrame(d)

data = gen_data(1000000)
data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>genre</th>
      <th>val</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>C</td>
      <td>54</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>D</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>D</td>
      <td>42</td>
    </tr>
    <tr>
      <th>4</th>
      <td>C</td>
      <td>91</td>
    </tr>
  </tbody>
</table>
</div>




```python
def transform(data):
    data.loc[:, "new_val"] = data.val.apply(lambda x: x + 1 if x % 2 else x - 1)
```


```python
%timeit -n 1 transform(data)
```

    284 ms ± 8.95 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 2. 用Cython编写C扩展
试试用我们的老朋友Cython来写一下 `x + 1 if x % 2 else x - 1` 这个函数。平均运行时间降低到了202ms，果然速度变快了。性能大约提升了1.4倍，离40倍的flag还差的好远[捂脸]。


```python
%load_ext cython
```


```cython
%%cython
cpdef int _transform(int x):
    if x % 2:
        return x + 1
    return x - 1

def transform(data):
    data.loc[:, "new_val"] = data.val.apply(_transform)
```


```python
%timeit -n 1 transform(data)
```

    202 ms ± 13.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 3. 减少类型转换
为了减少C和Python之间的类型转换，我们直接把'val'这一列作为Numpy数组传递给Cython函数，注意区分cnp和np。平均运行时间直接降到10.8毫秒，性能大约提升了26倍，仿佛看到了一丝希望。


```cython
%%cython
import numpy as np
cimport numpy as cnp
ctypedef cnp.int_t DTYPE_t

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

def transform(data):
    data.loc[:, "new_val"] = _transform(data.val.values)
```


```python
%timeit -n 1 transform(data)
```

    10.8 ms ± 512 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 4. 使用不安全的数组
利用@cython.boundscheck(False)，@cython.wraparound(False)装饰器关闭数组的边界检查和负下标处理，平均运行时间变为5.9毫秒。性能提升了42倍左右，顺利完成任务。


```cython
%%cython
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

def transform(data):
    data.loc[:, "new_val"] = _transform(data.val.values)
```


```python
%timeit -n 1 transform(data)
```

    6.76 ms ± 545 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)

