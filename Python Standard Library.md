# 用Python标准库写出高效的代码
作者: tushushu  
项目地址: https://github.com/tushushu/flying-python

## 1. bisect - 二分查找
给定一个列表对象，我们要对目标元素进行查找，返回其在列表中的下标。  
* 首先想到的是Python列表的index方法。建立一个长度为10000的升序列表，编写search函数使用index方式把里面的每一个元素查找一遍，平均运行时间437毫秒。
* 使用bisect模块的bisect_left，也就是我们熟知的二分查找。编写fast_search函数，平均运行时间3.94毫秒，性能提升了110倍！


```python
import bisect
```


```python
def search(nums):
    for x in nums:
        nums.index(x)
```


```python
def fast_search(nums):
    for x in nums:
        bisect.bisect_left(nums, x)
```


```python
arr = list(range(10000))
```


```python
%timeit -n 1 search(arr)
```

    437 ms ± 12.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%timeit -n 1 fast_search(arr)
```

    3.94 ms ± 407 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 2. Counter - 高效计数
给定一个列表对象，我们要统计其中的每个不重复的元素出现了多少次，返回一个字典对象。  
* 创建一个长度为10000，元素为1-3之间的随机数的列表。编写count函数，创建一个空字典，用for循环遍历该列表，将计数结果写入字典。平均运行时间937微秒。
* 使用collections模块的Counter，编写fast_count函数，一行代码搞定。平均运行时间494微秒，性能几乎是原来的2倍。


```python
from collections import Counter
from random import randint
```


```python
def count(nums):
    res = dict()
    for x in nums:
        if x in res:
            res[x] += 1
        else:
            res[x] = 0
    return x
```


```python
def fast_count(nums):
    return Counter(nums)
```


```python
nums = [randint(1, 3) for _ in range(10000)]
```


```python
%timeit -n 1 count(nums)
```

    937 µs ± 153 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%timeit -n 1 fast_count(nums)
```

    494 µs ± 240 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 3. heapq - 堆
给定一个列表对象，返回该列表中最小的3个元素。
* 创建一个长度为10000的列表，对元素进行随机打乱。编写top_3函数，对列表进行排序，返回前3个元素。平均运行时间2.03毫秒。
* 使用heapq模块，也就是我们熟悉的堆，编写fast_top_3函数。平均运行时间296微秒，性能提升了6.8倍。


```python
import heapq
from random import shuffle
```


```python
def top_3(nums):
    return sorted(nums)[:3]
```


```python
def fast_top_3(nums):
    return heapq.nsmallest(3, nums)
```


```python
nums = list(range(10000))
shuffle(nums)
```


```python
%timeit -n 1 top_3(nums)
```

    2.03 ms ± 236 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%timeit -n 1 fast_top_3(nums)
```

    296 µs ± 56.2 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 4. itemgetter - 批量get元素
给定一个字典和一个列表，列表中包含一个或多个字典中的key，返回对应的values。
* 创建一个元素数量为10万的字典，从字典的key中随机抽样10万，形成一个长度为1万的列表。编写get_items函数，平均运行时间1.12毫秒
* 使用itemgetter批量读取这些元素，编写fast_get_items函数，平均运行时间836微秒，性能是原来的1.3倍。



```python
from operator import itemgetter
from random import choices
```


```python
def get_items(data, keys):
    return [data[x] for x in keys]
```


```python
def fast_get_items(data, keys):
    return itemgetter(*keys)(data)
```


```python
data= dict(enumerate(range(100000)))
keys = choices(list(data.keys()), k=10000)
```


```python
%timeit -n 5 get_items(data, keys)
```

    1.12 ms ± 354 µs per loop (mean ± std. dev. of 7 runs, 5 loops each)



```python
%timeit -n 5 fast_get_items(data, keys)
```

    836 µs ± 287 µs per loop (mean ± std. dev. of 7 runs, 5 loops each)


## 5. lru_cache - 空间换时间
给定数字n，返回长度为n的斐波那且数列
* 使用递归方式，编写fib函数，并用fib_seq函数对其进行循环调用。令n等于20，平均运行时间3.28ms。
* 使用@lru_cache语法糖，将已经计算出来的结果缓存起来，比如fib(4)，计算fib(5)的时候可以直接调用缓存的fib(4)。平均运行时间144微秒，性能提升了22倍。


```python
from functools import lru_cache
```


```python
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def fib_seq(n):
    return [fib(x) for x in range(n)]
```


```python
@lru_cache(maxsize=None)
def fast_fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def fast_fib_seq(n):
    return [fast_fib(x) for x in range(n)]
```


```python
%timeit -n 5 fib_seq(20)
```

    3.28 ms ± 220 µs per loop (mean ± std. dev. of 7 runs, 3 loops each)



```python
%timeit -n 5 fast_fib_seq(20)
```

    The slowest run took 524.07 times longer than the fastest. This could mean that an intermediate result is being cached.
    144 µs ± 347 µs per loop (mean ± std. dev. of 7 runs, 3 loops each)



```python

```
