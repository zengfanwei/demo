# coding=utf-8

import os
import sys

# os.makedirs('ll' + 'kk')


def add(a, b):
	print a + b


if __name__ == "__main__":
	print sys.argv
	add(sys.argv[1], sys.argv[2])
