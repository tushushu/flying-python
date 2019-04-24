"""
@Author: tushushu
@Date: 2019-04-24 16:15:03
"""
import pyximport; pyximport.install()
from hello import say_hello_to

if __name__ == "__main__":
    say_hello_to("world")

