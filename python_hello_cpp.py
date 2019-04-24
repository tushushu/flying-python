"""
@Author: tushushu
@Date: 2019-04-24 16:15:03
"""
import pyx2cpp; pyx2cpp.install()
from hello import say_hello_to

if __name__ == "__main__":
    print(say_hello_to("world"))

