# Python多任务处理(多进程篇)
作者: tushushu  
项目地址: https://github.com/tushushu/flying-python

## 多进程处理CPU密集型任务
CPU密集型任务的特点是要进行大量的计算，消耗CPU资源，比如计算圆周率、对视频进行高清解码等等，全靠CPU的运算能力。一个线程执行CPU密集型任务的时候，CPU处于忙碌状态，运行1000个字节码之后GIL会被释放给其他线程，加上切换线程的时间有可能会比串行代码更慢。在Python多任务处理(多线程篇)，我们试图用多线程执行CPU密集型任务，然而并没有性能上的提升。现在我们试一下用多进程来处理CPU密集型任务。

### 1. 建立进程池


```python
from concurrent.futures import ProcessPoolExecutor
from time import sleep, time
import os
print("CPU核数为%s个!" % os.cpu_count())
```

    CPU核数为8个!



```python
# Worker数量
N = 8
# 建立进程池
pool = ProcessPoolExecutor(max_workers=N)
```

### 2. 定义一个CPU密集型函数
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

### 3. 使用串行的方式处理
遍历一个列表的所有元素，执行func函数。


```python
def process_array(arr):
    for x in arr:
        cpu_bound_func(x)
```

### 4. 使用多进程处理
通过线程池的map方法，可以将同一个函数作用在列表中的所有元素上。


```python
def fast_process_array(arr):
    for x in pool.map(cpu_bound_func, arr):
        pass
```

### 5. 计算函数运行时间
- 串行版本的运行时间5.7秒
- 多进程版本的运行时间1.6秒


```python
def time_it(fn, *args):
    start = time()
    fn(*args)
    print("%s版本的运行时间为 %.5f 秒!" % (fn.__name__, time() - start))
```


```python
time_it(process_array, [10**7 for _ in range(8)])
```

    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    Finish sum from 1 to 10000000!
    process_array版本的运行时间为 5.74394 秒!



```python
time_it(fast_process_array, [10**7 for _ in range(8)])
```

    fast_process_array版本的运行时间为 1.62266 秒!

