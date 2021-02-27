# 10分钟入门Cython
作者: tushushu  
项目地址: https://github.com/tushushu/flying-python

## 1. Cython是什么? 
Cython是一个编程语言，它通过类似Python的语法来编写C扩展并可以被Python调用.既具备了Python快速开发的特点，又可以让代码运行起来像C一样快，同时还可以方便地调用C library。

## 2. 如何安装Cython?
跟大多数的Python库不同，Cython需要一个C编译器，在不同的平台上配置方法也不一样。
### 2.1 配置gcc
- **windows**  
安装MingW-w64编译器：``conda install libpython m2w64-toolchain -c msys2``  
在Python安装路径下找到\Lib\distutils文件夹，创建distutils.cfg写入如下内容：  
``[build] compiler=mingw32``

- **macOS**   
安装XCode即可  

- **linux:**  
gcc一般都是配置好的，如果没有就执行这条命令：  ``sudo apt-get install build-essential``  


### 2.2 安装cython库
- 如果没安装Anaconda：  ``pip install cython`` 
- 如果安装了Anaconda：  ``conda install cython``

## 3. 在Jupyter Notebook上使用Cython 
- 首先加载Cython扩展，使用魔术命令  ``%load_ext Cython``
- 接下来运行Cython代码，使用魔术命令  ``%%cython``


```python
%load_ext Cython
```


```cython
%%cython
# 对1~100的自然数进行求和
total = 0
for i in range(1, 101):
    total += i
print(total)
```

    5050


## 4. 试试Cython到底有多快
- Python函数，运行时间261 ns
- Cython函数，运行时间44.1 ns  

运行时间竟然只有原来的五分之一左右，秘诀就在于参数x使用了静态类型int，避免了类型检查的耗时。

### 4.1 Python函数


```python
def f(x):
    return x ** 2 - x
```


```python
%timeit f(100)
```

    261 ns ± 8.78 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)


### 4.2 Cython函数


```cython
%%cython
def g(int x):
    return x ** 2 - x
```


```python
%timeit g(100)
```

    44.1 ns ± 1.09 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)


## 参考文章
部分内容引用自 - [Cython官方文档](http://docs.cython.org/en/latest/index.html)


```python

```
