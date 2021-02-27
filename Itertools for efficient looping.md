# Python Itertools - 高效的循环
作者: tushushu  
项目地址: https://github.com/tushushu/flying-python  

Python官方文档用"高效的循环"来形容itertools模块，有些tools会带来性能提升，而另外一些tools并不快，只是会节省一些开发时间而已，如果滥用还会导致代码可读性变差。我们不妨把itertools的兄弟们拉出来溜溜。


## 1. 数列累加
给定一个列表An，返回数列累加和Sn。
举例说明：
* 输入: [1, 2, 3, 4, 5]
* 返回: [1, 3, 6, 10, 15]  

使用accumulate，性能提升了2.5倍


```python
from itertools import accumulate
```


```python
def _accumulate_list(arr):
    tot = 0
    for x in arr:
        tot += x
        yield tot

def accumulate_list(arr):
    return list(_accumulate_list(arr))
```


```python
def fast_accumulate_list(arr):
    return list(accumulate(arr))
```


```python
arr = list(range(1000))
```


```python
%timeit accumulate_list(arr)
```

    61 µs ± 2.91 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)



```python
%timeit fast_accumulate_list(arr)
```

    21.3 µs ± 811 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)


## 2. 选择数据
给定一个列表data，一个用0/1表示的列表selectors，返回被选择的数据。
举例说明：
* 输入: [1, 2, 3, 4, 5], [0, 1, 0, 1, 0]
* 返回: [2, 4]  

使用compress，性能提升了2.8倍


```python
from itertools import compress
from random import randint
```


```python
def select_data(data, selectors):
    return [x for x, y in zip(data, selectors) if y]
```


```python
def fast_select_data(data, selectors):
    return list(compress(data, selectors))
```


```python
data = list(range(10000))
selectors = [randint(0, 1) for _ in range(10000)]
```


```python
%timeit select_data(data, selectors)
```

    341 µs ± 17.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



```python
%timeit fast_select_data(data, selectors)
```

    130 µs ± 3.19 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


## 3. 组合
给定一个列表arr和一个数字k，返回从arr中选择k个元素的所有情况。
举例说明：
* 输入: [1, 2, 3], 2
* 返回: [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)] 

使用permutations，性能提升了10倍


```python
from itertools import permutations
```


```python
def _get_permutations(arr, k, i):
    if i == k:
        return [arr[:k]]
    res = []
    for j in range(i, len(arr)):
        arr_cpy = arr.copy()
        arr_cpy[i], arr_cpy[j] = arr_cpy[j], arr_cpy[i]
        res += _get_permutations(arr_cpy, k, i + 1)
    return res
    
def get_permutations(arr, k):
    return _get_permutations(arr, k, 0)
```


```python
def fast_get_permutations(arr, k):
    return list(permutations(arr, k))
```


```python
arr = list(range(10))
k = 5
```


```python
%timeit -n 1 get_permutations(arr, k)
```

    15.5 ms ± 1.96 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%timeit -n 1 fast_get_permutations(arr, k)
```

    1.56 ms ± 284 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)


## 4. 筛选数据
给定一个列表arr，筛选出所有的偶数。
举例说明：
* 输入: [3, 1, 4, 5, 9, 2]
* 返回: [(4, 2] 

使用filterfalse，性能反而会变慢，所以不要迷信itertools。


```python
from itertools import filterfalse
```


```python
def get_even_nums(arr):
    return [x for x in arr if x % 2 == 0]
```


```python
def fast_get_even_nums(arr):
    return list(filterfalse(lambda x: x % 2, arr))
```


```python
arr = list(range(10000))
```


```python
%timeit get_even_nums(arr)
```

    417 µs ± 18.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



```python
%timeit fast_get_even_nums(arr)
```

    823 µs ± 22.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


## 5. 条件终止
给定一个列表arr，依次对列表的所有数字进行求和，若遇到某个元素大于target之后则终止求和，返回这个和。
举例说明：
* 输入: [1, 2, 3, 4, 5], 3
* 返回: 6 (4 > 3，终止)

使用takewhile，性能反而会变慢，所以不要迷信itertools。


```python
from itertools import takewhile
```


```python
def cond_sum(arr, target):
    res = 0
    for x in arr:
        if x > target:
            break
        res += x
    return res
```


```python
def fast_cond_sum(arr, target):
    return sum(takewhile(lambda x: x <= target, arr))
```


```python
arr = list(range(10000))
target = 5000
```


```python
%timeit cond_sum(arr, target)
```

    245 µs ± 11.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



```python
%timeit fast_cond_sum(arr, target)
```

    404 µs ± 13.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


## 6. 循环嵌套
给定列表arr1，arr2，返回两个列表的所有元素两两相加的和。
举例说明：
* 输入: [1, 2], [4, 5]
* 返回: [1 + 4， 1 + 5， 2 + 4， 2 + 5]

使用product，性能提升了1.25倍。


```python
from itertools import product
```


```python
def _cross_sum(arr1, arr2):
    for x in arr1:
        for y in arr2:
            yield x + y

def cross_sum(arr1, arr2):
    return list(_cross_sum(arr1, arr2))
```


```python
def fast_cross_sum(arr1, arr2):
    return [x + y for x, y in product(arr1, arr2)]
```


```python
arr1 = list(range(100))
arr2 = list(range(100))
```


```python
%timeit cross_sum(arr1, arr2)
```

    484 µs ± 16.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



```python
%timeit fast_cross_sum(arr1, arr2)
```

    373 µs ± 11.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


## 7. 二维列表转一维列表
给定二维列表arr，转为一维列表
举例说明：
* 输入: [[1, 2], [3, 4]]
* 返回: [1, 2, 3, 4]

使用chain，性能提升了6倍。


```python
from itertools import chain
```


```python
def _flatten(arr2d):
    for arr in arr2d:
        for x in arr:
            yield x

def flatten(arr2d):
    return list(_flatten(arr2d))
```


```python
def fast_flatten(arr2d):
    return list(chain(*arr2d))
```


```python
arr2d = [[x + y * 100 for x in range(100)] for y in range(100)]
```


```python
%timeit flatten(arr2d)
```

    379 µs ± 15.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



```python
%timeit fast_flatten(arr2d)
```

    66.9 µs ± 3.43 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)



```python

```
