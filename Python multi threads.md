# Python多任务处理(多线程篇)
作者: tushushu  
项目地址: https://github.com/tushushu/flying-python

## 1. GIL

熟悉python的都知道，在C语言写的python解释器中存在全局解释器锁，由于全局解释器锁的存在，在同一时间内，python解释器只能运行一个线程的代码，这大大影响了python多线程的性能。而这个解释器锁由于历史原因，现在几乎无法消除。 
  
python GIL 之所以会影响多线程等性能，是因为在多线程的情况下，只有当线程获得了一个全局锁的时候，那么该线程的代码才能运行，而全局锁只有一个，所以使用python多线程，在同一时刻也只有一个线程在运行，因此在即使在多核的情况下也只能发挥出单核的性能。 


## 2. 多线程处理IO密集型任务
IO密集型任务指的是系统的CPU性能相对硬盘、内存要好很多，此时，系统运作，大部分的状况是CPU在等I/O (硬盘/内存) 的读/写操作，此时CPU Loading并不高。涉及到网络、磁盘IO的任务都是IO密集型任务。一个线程执行IO密集型任务的时候，CPU处于闲置状态，因此GIL会被释放给其他线程，从而缩短了总体的等待运行时间。


```python
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time
```


```python
# Worker数量
N = 4
# 建立线程池
pool = ThreadPoolExecutor(max_workers=N)
```

### 2.1 定义一个IO密集型函数
该函数会“睡眠”x秒。


```python
def io_bound_func(x):
    sleep(x)
    print("Sleep for %d seconds." % x)
```

### 2.2 使用串行的方式处理
遍历一个列表的所有元素，执行func函数。


```python
def process_array(arr):
    for x in arr:
        io_bound_func(x)
```

### 2.3 使用多线程处理
通过线程池的map方法，可以将同一个函数作用在列表中的所有元素上。


```python
def fast_process_array(arr):
    for x in pool.map(io_bound_func, arr):
        pass
```

### 2.4 计算函数运行时间
- 串行版本的运行时间 = 1 + 2 + 3 = 6秒  
- 多线程版本的运行时间 = max(1, 2, 3) = 3秒


```python
def time_it(fn, *args):
    start = time()
    fn(*args)
    print("%s版本的运行时间为 %.5f 秒!" % (fn.__name__, time() - start))
```


```python
time_it(process_array, [1, 2, 3])
```

    Sleep for 1 seconds.
    Sleep for 2 seconds.
    Sleep for 3 seconds.
    process_array版本的运行时间为 6.00883 秒!



```python
time_it(fast_process_array, [1, 2, 3])
```

    Sleep for 1 seconds.
    Sleep for 2 seconds.
    Sleep for 3 seconds.
    fast_process_array版本的运行时间为 3.00300 秒!


### 3. 多线程CPU密集型任务
CPU密集型任务的特点是要进行大量的计算，消耗CPU资源，比如计算圆周率、对视频进行高清解码等等，全靠CPU的运算能力。一个线程执行CPU密集型任务的时候，CPU处于忙碌状态，运行1000个字节码之后GIL会被释放给其他线程，加上切换线程的时间有可能会比串行代码更慢。

### 3.1 定义一个CPU密集型函数
该函数会对[1, x]之间的整数进行求和。


```python
def cpu_bound_func(x):
    tot = 0
    a = 1
    while a <= x:
        tot += x
        a += 1
    print("Finish sum from 1 to %d!" % x)
    return tot
```

### 3.2 使用串行的方式处理
遍历一个列表的所有元素，执行func函数。


```python
def process_array(arr):
    for x in arr:
        cpu_bound_func(x)
```

### 3.3 使用多线程处理
通过线程池的map方法，可以将同一个函数作用在列表中的所有元素上。


```python
def fast_process_array(arr):
    for x in pool.map(cpu_bound_func, arr):
        pass
```

### 3.4 计算函数运行时间
- 串行版本的运行时间2.1秒
- 多线程版本的运行时间2.2秒


```python
def time_it(fn, *args):
    start = time()
    fn(*args)
    print("%s版本的运行时间为 %.5f 秒!" % (fn.__name__, time() - start))
```


```python
time_it(process_array, [10**7, 10**7, 10**7])
```

    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    process_array版本的运行时间为 2.10489 秒!



```python
time_it(fast_process_array, [10**7, 10**7, 10**7])
```

    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    fast_process_array版本的运行时间为 2.20897 秒!


## 参考文章
https://www.jianshu.com/p/c75ed8a6e9af  
https://www.cnblogs.com/tusheng/articles/10630662.html


```python

```
