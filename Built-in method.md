# 使用内置方法优化Python性能
作者: tushushu  
项目地址: https://github.com/tushushu/flying-python

Python程序运行太慢的一个可能的原因是没有尽可能的调用内置方法，下面通过5个例子来演示如何用内置方法提升Python程序的性能。

## 1. 数组求平方和
输入一个列表，要求计算出该列表中数字的的平方和。最终性能提升了1.4倍。

首先创建一个长度为10000的列表。


```python
arr = list(range(10000))
```

### 1.1 最常规的写法
while循环遍历列表求平方和。平均运行时间2.97毫秒。


```python
def sum_sqr_0(arr):
    res = 0
    n = len(arr)
    i = 0
    while i < n:
        res += arr[i] ** 2
        i += 1
    return res
```


```python
%timeit sum_sqr_0(arr)
```

    2.97 ms ± 36.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### 1.2 for range代替while循环
避免i += 1的变量类型检查带来的额外开销。平均运行时间2.9毫秒。


```python
def sum_sqr_1(arr):
    res = 0
    for i in range(len(arr)):
        res += arr[i] ** 2
    return res
```


```python
%timeit sum_sqr_1(arr)
```

    2.9 ms ± 137 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### 1.3 for x in arr代替for range
避免arr[i]的变量类型检查带来的额外开销。平均运行时间2.59毫秒。


```python
def sum_sqr_2(arr):
    res = 0
    for x in arr:
        res += x ** 2
    return res
```


```python
%timeit sum_sqr_2(arr)
```

    2.59 ms ± 89 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### 1.4 sum函数套用map函数
平均运行时间2.36毫秒


```python
def sum_sqr_3(arr):
    return sum(map(lambda x: x**2, arr))
```


```python
%timeit sum_sqr_3(arr)
```

    2.36 ms ± 15.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### 1.5 sum函数套用生成器表达式
生成器表达式如果作为某个函数的参数，则可以省略掉()。平均运行时间2.35毫秒。


```python
def sum_sqr_4(arr):
    return sum(x ** 2 for x in arr)
```


```python
%timeit sum_sqr_4(arr)
```

    2.35 ms ± 107 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### 1. 6 sum函数套用列表推导式
平均运行时间2.06毫秒。


```python
def sum_sqr_5(arr):
    return sum([x ** 2 for x in arr])
```


```python
%timeit sum_sqr_5(arr)
```

    2.06 ms ± 27.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


## 2. 字符串拼接
输入一个列表，要求将列表中的字符串的前3个字符都拼接为一个字符串。最终性能提升了2.1倍。

首先创建一个列表，生成10000个随机长度和内容的字符串。


```python
from random import randint

def random_letter():
    return chr(ord('a') + randint(0, 25))

def random_letters(n):
    return "".join([random_letter() for _ in range(n)])

strings = [random_letters(randint(1, 10)) for _ in range(10000)]
```

### 2.1 最常规的写法
while循环遍历列表，对字符串进行拼接。平均运行时间1.86毫秒。


```python
def concat_strings_0(strings):
    res = ""
    n = len(strings)
    i = 0
    while i < n:
        res += strings[i][:3]
        i += 1
    return res
```


```python
%timeit concat_strings_0(strings)
```

    1.86 ms ± 74.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 2.2 for range代替while循环
避免i += 1的变量类型检查带来的额外开销。平均运行时间1.55毫秒。


```python
def concat_strings_1(strings):
    res = ""
    for i in range(len(strings)):
        res += strings[i][:3]
    return res
```


```python
%timeit concat_strings_1(strings)
```

    1.55 ms ± 32.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 2.3 for x in strings代替for range
避免strings[i]的变量类型检查带来的额外开销。平均运行时间1.32毫秒。


```python
def concat_strings_2(strings):
    res = ""
    for x in strings:
        res += x[:3]
    return res
```


```python
%timeit concat_strings_2(strings)
```

    1.32 ms ± 19.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 2.4 .join方法套用生成器表达式
平均运行时间1.06毫秒。


```python
def concat_strings_3(strings):
    return "".join(x[:3] for x in strings)
```


```python
%timeit concat_strings_3(strings)
```

    1.06 ms ± 15.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 2.5 .join方法套用列表解析式
平均运行时间0.85毫秒。


```python
def concat_strings_4(strings):
    return "".join([x[:3] for x in strings])
```


```python
%timeit concat_strings_4(strings)
```

    858 µs ± 14.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


## 3. 筛选奇数

输入一个列表，要求筛选出该列表中的所有奇数。最终性能提升了3.6倍。

首先创建一个长度为10000的列表。


```python
arr = list(range(10000))
```

### 3.1 最常规的写法
创建一个空列表res，while循环遍历列表，将奇数append到res中。平均运行时间1.03毫秒。


```python
def filter_odd_0(arr):
    res = []
    i = 0
    n = len(arr)
    while i < n:
        if arr[i] % 2:
            res.append(arr[i])
        i += 1
    return res
```


```python
%timeit filter_odd_0(arr)
```

    1.03 ms ± 34.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 3.2 for range代替while循环
避免i += 1的变量类型检查带来的额外开销。平均运行时间0.965毫秒。


```python
def filter_odd_1(arr):
    res = []
    for i in range(len(arr)):
        if arr[i] % 2:
            res.append(arr[i])
        i += 1
    return res
```


```python
%timeit filter_odd_1(arr)
```

    965 µs ± 4.02 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 3.3 for x in arr代替for range
避免arr[i]的变量类型检查带来的额外开销。平均运行时间0.430毫秒。


```python
def filter_odd_2(arr):
    res = []
    for x in arr:
        if x % 2:
            res.append(x)
    return res
```


```python
%timeit filter_odd_2(arr)
```

    430 µs ± 9.25 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 3.4 list套用filter函数
平均运行时间0.763毫秒。注意filter函数很慢，在Python 3.6里非常鸡肋。


```python
def filter_odd_3(arr):
    return list(filter(lambda x: x % 2, arr))
```


```python
%timeit filter_odd_3(arr)
```

    763 µs ± 15.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 3.5 list套用生成器表达式
平均运行时间0.398毫秒。


```python
def filter_odd_4(arr):
    return list((x for x in arr if x % 2))
```


```python
%timeit filter_odd_4(arr)
```

    398 µs ± 16.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 3.6 带条件的列表推导式
平均运行时间0.290毫秒。


```python
def filter_odd_5(arr):
    return [x for x in arr if x % 2]
```


```python
%timeit filter_odd_5(arr)
```

    290 µs ± 5.54 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


## 4. 两个数组相加

输入两个长度相同的列表，要求计算出两个列表对应位置的数字之和，返回一个与输入长度相同的列表。最终性能提升了2.7倍。

首先生成两个长度为10000的列表。


```python
arr1 = list(range(10000))
arr2 = list(range(10000))
```

### 4.1 最常规的写法
创建一个空列表res，while循环遍历列表，将两个列表对应的元素之和append到res中。平均运行时间1.23毫秒。


```python
def arr_sum_0(arr1, arr2):
    i = 0
    n = len(arr1)
    res = []
    while i < n:
        res.append(arr1[i] + arr2[i])
        i += 1
    return res
```


```python
%timeit arr_sum_0(arr1, arr2)
```

    1.23 ms ± 3.77 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 4.2 for range代替while循环
避免i += 1的变量类型检查带来的额外开销。平均运行时间0.997毫秒。


```python
def arr_sum_1(arr1, arr2):
    res = []
    for i in range(len(arr1)):
        res.append(arr1[i] + arr2[i])
    return res
```


```python
%timeit arr_sum_1(arr1, arr2)
```

    997 µs ± 7.42 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 4.3 for i, x in enumerate代替for range
部分避免arr[i]的变量类型检查带来的额外开销。平均运行时间0.799毫秒。


```python
def arr_sum_2(arr1, arr2):
    res = arr1.copy()
    for i, x in enumerate(arr2):
        res[i] += x
    return res
```


```python
%timeit arr_sum_2(arr1, arr2)
```

    799 µs ± 16.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 4.4 for x, y in zip代替for range
避免arr[i]的变量类型检查带来的额外开销。平均运行时间0.769毫秒。


```python
def arr_sum_3(arr1, arr2):
    res = []
    for x, y in zip(arr1, arr2):
        res.append(x + y)
    return res
```


```python
%timeit arr_sum_3(arr1, arr2)
```

    769 µs ± 12.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 4.5 列表推导式套用zip
平均运行时间0.462毫秒。


```python
def arr_sum_4(arr1, arr2):
    return [x + y for x, y in zip(arr1, arr2)]
```


```python
%timeit arr_sum_4(arr1, arr2)
```

    462 µs ± 3.43 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


## 5. 两个列表相同元素的数量
输入两个列表，要求统计两个列表相同元素的数量。其中每个列表内的元素都是不重复的。最终性能提升了5000倍。

首先创建两个列表，并将元素的顺序打乱。


```python
from random import shuffle
arr1 = list(range(2000))
shuffle(arr1)
arr2 = list(range(1000, 3000))
shuffle(arr2)
```

### 5.1 最常规的写法
while循环嵌套，判断元素arr1[i]是否等于arr2[j]，平均运行时间338毫秒。


```python
def n_common_0(arr1, arr2):
    res = 0
    i = 0
    m = len(arr1)
    n = len(arr2)
    while i < m:
        j = 0
        while j < n:
            if arr1[i] == arr2[j]:
                res += 1
            j += 1
        i += 1
    return res
```


```python
%timeit n_common_0(arr1, arr2)
```

    338 ms ± 7.81 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


### 5.2 for range代替while循环
避免i += 1的变量类型检查带来的额外开销。平均运行时间233毫秒。


```python
def n_common_1(arr1, arr2):
    res = 0
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            if arr1[i] == arr2[j]:
                res += 1
    return res
```


```python
%timeit n_common_1(arr1, arr2)
```

    233 ms ± 10.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


### 5.3 for x in arr代替for range
避免arr[i]的变量类型检查带来的额外开销。平均运行时间84.8毫秒。


```python
def n_common_2(arr1, arr2):
    res = 0
    for x in arr1:
        for y in arr2:
            if x == y:
                res += 1
    return res
```


```python
%timeit n_common_2(arr1, arr2)
```

    84.8 ms ± 1.38 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


### 5.4 使用if x in arr2代替内层循环
平均运行时间24.9毫秒。


```python
def n_common_3(arr1, arr2):
    res = 0
    for x in arr1:
        if x in arr2:
            res += 1
    return res
```


```python
%timeit n_common_3(arr1, arr2)
```

    24.9 ms ± 1.39 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


### 5.4 使用更快的算法
将数组用.sort方法排序，再进行单层循环遍历。把时间复杂度从O(n2)降低到O(nlogn)，平均运行时间0.239毫秒。


```python
def n_common_4(arr1, arr2):
    arr1.sort()
    arr2.sort()
    res = i = j = 0
    m, n = len(arr1), len(arr2)
    while i < m and j < n:
        if arr1[i] == arr2[j]:
            res += 1
            i += 1
            j += 1
        elif arr1[i] > arr2[j]:
            j += 1
        else:
            i += 1
    return res
```


```python
%timeit n_common_4(arr1, arr2)
```

    329 µs ± 12.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


### 5.5 使用更好的数据结构
将数组转为集合，求交集的长度。平均运行时间0.067毫秒。


```python
def n_common_5(arr1, arr2):
    return len(set(arr1) & set(arr2))
```


```python
%timeit n_common_5(arr1, arr2)
```

    67.2 µs ± 755 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)



```python

```
