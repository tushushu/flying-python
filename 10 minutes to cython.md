# 10分钟入门Cython
https://github.com/tushushu/flying-python

## 1. Cython是什么?
Cython是一个编程语言，它通过类似Python的语法来编写C扩展并可以被Python调用.既具备了Python快速开发的特点，又可以让代码运行起来像C一样快，同时还可以方便地调用C
library。

## 2. 如何安装Cython?
跟大多数的Python库不同，Cython需要一个C编译器，在不同的平台上配置方法也不一样。
### 2.1 配置gcc
- **windows**  
安装MingW-w64编译器：``conda install libpython m2w64-toolchain -c
msys2``  
在Python安装路径下找到\Lib\distutils文件夹，创建distutils.cfg写入如下内容：  
```
[build] 
compiler=mingw32
```

- **macOS**   
安装XCode即可  

- **linux:**
gcc一般都是配置好的，如果没有就执行这条命令：  ``sudo apt-get install build-essential``  


### 2.2 安装cython库
- 如果没安装Anaconda：  ``pip install cython`` 
- 如果安装了Anaconda：  ``conda
install cython``

## 3. 在Jupyter Notebook上使用Cython 
- 首先加载Cython扩展，使用魔术命令  ``%load_ext Cython``
- 接下来运行Cython代码，使用魔术命令  ``%%cython``

```python
%load_ext Cython
```

```python
%%cython
cdef int a = 0
for i in range(10):
    a += i
print(a)
```

## 4. 试试Cython到底有多快
- 常规Python函数，运行时间559 ns
- Cython def函数，声明一个Python函数，既可以在模块内调用，也可以在模块外调用。模块内运行时间524.2 ns，模块外运行时间512 ns
- Cython cpdef函数，声明一个C函数和一个Python wrapper，在模块内被当做C函数调用，在模块外被.py文件当做Python函数调用。模块内运行时间43.7
ns，模块外运行时间81.7 ns
- Cython cdef函数，声明一个C函数，不可以在模块外被Python调用。模块内运行时间34.8 ns

### 4.1 常规Python函数

```python
def f(x):
    return x ** 2 - x
```

```python
%timeit f(100)
```

### 4.2 Cython def函数

```python
%%cython
from time import time

def f1(x):
    return x ** 2 - x

n = 10000000
start = time()
for _ in range(n):
    f1(100)
end = time()
run_time = (end - start) / n * 1000 * 1000 * 1000
print("%.1f ns" % run_time)
```

```python
%timeit f1(100)
```

### 4.3 Cython cpdef函数

```python
%%cython
from time import time

cpdef long f2(long x):
    return x ** 2 - x

n = 10000000
start = time()
for _ in range(n):
    f2(100)
end = time()
run_time = (end - start) / n * 1000 * 1000 * 1000
print("%.1f ns" % run_time)
```

```python
%timeit f2(100)
```

### 4.4 Cython cdef函数

```python
%%cython
from time import time

cdef long f3(long x):
    return x ** 2 - x

n = 10000000
start = time()
for _ in range(n):
    f3(100)
end = time()
run_time = (end - start) / n * 1000 * 1000 * 1000
print("%.1f ns" % run_time)
```

## 5. 在Cython中使用Python对象 
- 常规Python函数，运行时间549微秒
- Python内置函数，运行时间104微秒
- Cython函数，运行时间51.6微秒

```python
A = list(range(10000))
```

### 5.1 常规Python函数

```python
def sum_list(A):
    ret = 0
    for x in A:
        ret += x
    return ret
```

```python
%timeit sum_list(A)
```

### 5.2 Python内置函数

```python
%timeit sum(A)
```

### 5.3 Cython函数

```python
%%cython
cpdef int sum_list_cython(A):
    cdef int ret, x
    for x in A:
        ret += x
    return ret
```

```python
%timeit sum_list_cython(A)
```

## 6. 在.pyx文件中使用Cython 
- 建立名为example.pyx的文件，键入如下代码
- 在控制台使用cythonize命令，将.pyx文件转为.c文件再编译为C模块

```python
from time import time

cdef long f4(long x):
    return x ** 2 - x

if __name__ == "__main__":
    cdef int x = 3
    print(f4(x))
```

## 参考文章
部分内容引用自 - [Cython官方文档](http://docs.cython.org/en/latest/index.html)
