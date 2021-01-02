import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def test_numpy():
    x = np.arange(-10, 10)
    print(x)


def print_environmental_stuff():
    print(os.uname())
    homepath = Path.home()
    print(homepath)
    print(homepath.absolute())
    print(f'sys.path={sys.path}')


def test_x11():
    x = np.linspace(start=-10, stop=10, num=100)
    y = x ** 2
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    test_numpy()
    print_environmental_stuff()
    test_x11()
