from itertools import combinations
import copy
import numpy as np
import random
import math
import matplotlib.pyplot as plt

random.seed(a=5)

distance_mtrx = [
    [0, 14, 4, 5, 22, 6, 7, 9, 7, 7, 2, 13, 15, 12, 11, 17, 11, 4, 18, 9, 8, 10, 9, 25, 11, 20, 19, 23, 32, 21, 29, 34,
     20, 18, 27, 18, 21, 12, 9, 15, 11, 21, 23, 18, 16, 31, 23, 26, 21, 20, 12, 100],
    [14, 0, 12, 7, 9, 15, 18, 12, 11, 19, 7, 11, 9, 19, 21, 11, 16, 13, 19, 23, 17, 11, 22, 20, 11, 13, 11, 17, 8, 11,
     8, 29, 14, 7, 14, 12, 18, 19, 11, 21, 20, 15, 13, 18, 14, 29, 21, 17, 24, 21, 19, 31],
    [4, 12, 0, 11, 12, 17, 7, 6, 12, 9, 4, 17, 21, 8, 12, 15, 23, 22, 16, 14, 19, 10, 8, 5, 17, 11, 21, 25, 23, 22, 19,
     21, 21, 16, 15, 19, 29, 31, 16, 19, 11, 21, 20, 24, 19, 21, 22, 27, 29, 33, 16, 21],
    [5, 7, 11, 0, 8, 11, 16, 5, 9, 7, 12, 9, 11, 15, 19, 11, 14, 13, 17, 22, 29, 26, 19, 13, 16, 27, 25, 23, 11, 19, 21,
     8, 17, 10, 15, 18, 27, 23, 20, 16, 14, 19, 11, 13, 22, 21, 21, 30, 19, 27, 25, 14],
    [22, 9, 12, 8, 0, 7, 8, 4, 9, 14, 12, 11, 15, 17, 9, 15, 17, 11, 16, 10, 21, 30, 21, 16, 12, 11, 17, 13, 11, 19, 11,
     16, 9, 23, 21, 22, 14, 17, 13, 11, 14, 18, 24, 28, 29, 30, 21, 25, 16, 11, 17, 24],
    [6, 15, 17, 11, 7, 0, 6, 4, 6, 24, 11, 27, 15, 19, 21, 23, 12, 17, 19, 22, 14, 10, 22, 26, 21, 27, 16, 13, 14, 11,
     8, 6, 18, 11, 21, 27, 11, 29, 22, 12, 17, 8, 11, 21, 30, 12, 16, 29, 22, 11, 15, 19],
    [7, 18, 7, 16, 8, 6, 0, 12, 8, 15, 9, 22, 12, 11, 16, 9, 6, 12, 14, 21, 27, 11, 23, 26, 21, 25, 11, 10, 13, 9, 7,
     16, 15, 13, 19, 21, 22, 18, 13, 16, 12, 13, 19, 21, 22, 17, 21, 21, 29, 24, 19, 11],
    [9, 12, 6, 5, 4, 4, 12, 0, 12, 14, 4, 12, 7, 9, 12, 11, 16, 18, 14, 10, 21, 27, 11, 14, 16, 11, 19, 21, 28, 31, 21,
     22, 26, 16, 8, 11, 15, 24, 29, 21, 20, 16, 11, 9, 24, 22, 15, 18, 13, 16, 13, 16],
    [7, 11, 12, 9, 9, 6, 8, 12, 0, 21, 25, 17, 14, 6, 21, 9, 11, 19, 12, 17, 14, 21, 29, 16, 11, 12, 24, 11, 12, 15, 8,
     11, 23, 21, 35, 21, 22, 31, 29, 21, 17, 13, 8, 16, 15, 7, 21, 9, 15, 12, 22, 21],
    [7, 19, 9, 7, 14, 24, 15, 14, 21, 0, 12, 11, 6, 13, 11, 16, 12, 11, 8, 9, 12, 16, 19, 31, 25, 27, 12, 21, 20, 31,
     21, 26, 24, 21, 36, 22, 16, 7, 15, 13, 6, 17, 14, 8, 15, 17, 12, 11, 21, 27, 23, 20],
    [2, 7, 4, 12, 12, 11, 9, 4, 25, 12, 0, 6, 7, 16, 13, 9, 17, 13, 20, 25, 21, 11, 12, 16, 22, 21, 23, 29, 32, 10, 11,
     13, 16, 12, 6, 10, 32, 21, 19, 16, 11, 32, 21, 18, 14, 12, 14, 13, 8, 11, 23, 14],
    [13, 11, 17, 9, 11, 27, 22, 12, 17, 11, 6, 0, 9, 12, 13, 11, 14, 18, 21, 23, 22, 12, 10, 16, 12, 19, 9, 17, 7, 10,
     17, 13, 21, 17, 24, 16, 13, 20, 28, 21, 26, 21, 15, 19, 11, 12, 17, 21, 22, 11, 9, 17],
    [15, 9, 21, 11, 15, 15, 12, 7, 14, 6, 7, 9, 0, 21, 8, 13, 19, 27, 16, 13, 11, 21, 22, 28, 11, 13, 15, 9, 7, 13, 11,
     17, 19, 28, 14, 18, 14, 16, 15, 19, 16, 13, 16, 17, 13, 18, 11, 16, 19, 24, 28, 31],
    [12, 19, 8, 15, 17, 19, 11, 9, 6, 13, 16, 12, 21, 0, 21, 11, 20, 8, 6, 13, 12, 19, 23, 11, 14, 16, 11, 17, 16, 13,
     11, 10, 21, 22, 31, 26, 28, 23, 16, 14, 13, 10, 7, 13, 16, 13, 20, 25, 17, 25, 22, 13],
    [11, 21, 12, 19, 9, 21, 16, 12, 21, 11, 13, 13, 8, 21, 0, 9, 7, 11, 12, 11, 24, 21, 12, 16, 25, 21, 17, 14, 7, 10,
     14, 11, 14, 22, 31, 29, 21, 13, 15, 18, 11, 12, 17, 14, 12, 6, 11, 12, 23, 8, 4, 11],
    [17, 11, 15, 11, 15, 23, 9, 11, 9, 16, 9, 11, 13, 11, 9, 0, 11, 21, 21, 34, 22, 11, 12, 11, 11, 21, 14, 11, 13, 12,
     12, 13, 14, 16, 12, 21, 41, 22, 12, 12, 33, 11, 9, 14, 12, 12, 15, 13, 12, 14, 19, 21],
    [11, 16, 23, 14, 17, 12, 6, 16, 11, 12, 17, 14, 19, 20, 7, 11, 0, 9, 7, 10, 12, 16, 14, 14, 21, 32, 23, 17, 11, 37,
     21, 11, 13, 16, 11, 16, 10, 9, 17, 14, 15, 12, 21, 12, 16, 16, 14, 13, 15, 9, 5, 11],
    [4, 13, 22, 13, 11, 17, 12, 18, 19, 11, 13, 18, 27, 8, 11, 21, 9, 0, 12, 11, 14, 12, 21, 26, 21, 29, 21, 20, 21, 23,
     16, 12, 13, 18, 9, 21, 8, 12, 18, 7, 27, 21, 16, 13, 11, 21, 25, 28, 21, 13, 8, 10],
    [18, 19, 16, 17, 16, 19, 14, 14, 12, 8, 20, 21, 16, 6, 12, 21, 7, 12, 0, 16, 21, 14, 17, 11, 13, 9, 8, 10, 12, 17,
     14, 27, 21, 31, 22, 20, 21, 24, 25, 12, 17, 14, 6, 9, 18, 11, 15, 12, 17, 11, 12, 7],
    [9, 23, 14, 22, 10, 22, 21, 10, 17, 9, 25, 23, 13, 13, 11, 34, 10, 11, 16, 0, 12, 6, 12, 13, 18, 9, 6, 12, 10, 31,
     21, 11, 10, 7, 14, 17, 11, 19, 21, 11, 13, 18, 21, 22, 13, 14, 17, 11, 18, 10, 21, 11],
    [8, 17, 19, 29, 21, 14, 27, 21, 14, 12, 21, 22, 11, 12, 24, 22, 12, 14, 21, 12, 0, 7, 10, 8, 13, 11, 27, 21, 20, 11,
     17, 25, 27, 18, 21, 21, 18, 14, 8, 11, 9, 11, 8, 11, 14, 10, 12, 14, 11, 21, 9, 21],
    [10, 11, 10, 26, 30, 10, 11, 27, 21, 16, 11, 12, 21, 19, 21, 11, 16, 12, 14, 6, 7, 0, 21, 32, 11, 10, 8, 10, 12, 16,
     8, 19, 7, 12, 14, 16, 12, 11, 17, 23, 21, 25, 28, 31, 26, 13, 12, 16, 17, 12, 12, 11],
    [9, 22, 8, 19, 21, 22, 23, 11, 29, 19, 12, 10, 22, 23, 12, 12, 14, 21, 17, 12, 10, 21, 0, 10, 6, 17, 9, 10, 11, 16,
     12, 15, 17, 21, 11, 14, 12, 11, 26, 28, 22, 12, 11, 26, 13, 11, 11, 23, 8, 7, 19, 9],
    [25, 20, 5, 13, 16, 26, 26, 14, 16, 31, 16, 16, 28, 11, 16, 11, 14, 26, 11, 13, 8, 32, 10, 0, 12, 18, 15, 11, 11,
     17, 15, 12, 41, 9, 7, 10, 11, 15, 26, 21, 24, 15, 8, 12, 9, 13, 16, 12, 24, 11, 21, 27],
    [11, 11, 17, 16, 12, 21, 21, 16, 11, 25, 22, 12, 11, 14, 25, 11, 21, 21, 13, 18, 13, 11, 6, 12, 0, 11, 9, 11, 17,
     12, 14, 11, 21, 31, 12, 16, 11, 17, 12, 9, 7, 10, 9, 21, 14, 11, 13, 11, 21, 11, 10, 8],
    [20, 13, 11, 27, 11, 27, 25, 11, 12, 27, 21, 19, 13, 16, 21, 21, 32, 29, 9, 9, 11, 10, 17, 18, 11, 0, 8, 17, 15, 31,
     18, 11, 12, 16, 12, 17, 12, 21, 12, 14, 19, 12, 18, 11, 15, 14, 21, 18, 16, 12, 7, 12],
    [19, 11, 21, 25, 17, 16, 11, 19, 24, 12, 23, 9, 15, 11, 17, 14, 23, 21, 8, 6, 27, 8, 9, 15, 9, 8, 0, 21, 11, 11, 15,
     16, 12, 11, 14, 11, 19, 21, 14, 11, 19, 7, 9, 12, 15, 31, 21, 11, 21, 15, 17, 14],
    [23, 17, 25, 23, 13, 13, 10, 21, 11, 21, 29, 17, 9, 17, 14, 11, 17, 20, 10, 12, 21, 10, 10, 11, 11, 17, 21, 0, 10,
     9, 15, 11, 12, 6, 10, 21, 19, 8, 15, 14, 12, 10, 17, 9, 17, 12, 14, 16, 12, 17, 11, 22],
    [32, 8, 23, 11, 11, 14, 13, 28, 12, 20, 32, 7, 7, 16, 7, 13, 11, 21, 12, 10, 20, 12, 11, 11, 17, 15, 11, 10, 0, 9,
     12, 11, 12, 9, 10, 11, 12, 17, 9, 4, 15, 17, 15, 19, 11, 10, 9, 15, 16, 17, 15, 12],
    [21, 11, 22, 19, 19, 11, 9, 31, 15, 31, 10, 10, 13, 13, 10, 12, 37, 23, 17, 31, 11, 16, 16, 17, 12, 31, 11, 9, 9, 0,
     11, 21, 21, 17, 14, 21, 18, 11, 17, 13, 15, 11, 27, 10, 11, 12, 16, 14, 11, 12, 9, 8],
    [29, 8, 19, 21, 11, 8, 7, 21, 8, 21, 11, 17, 11, 11, 14, 12, 21, 16, 14, 21, 17, 8, 12, 15, 14, 18, 15, 15, 12, 11,
     0, 12, 13, 16, 9, 7, 11, 10, 7, 13, 11, 25, 11, 11, 15, 9, 7, 19, 8, 6, 10, 12],
    [34, 29, 21, 8, 16, 6, 16, 22, 11, 26, 13, 13, 17, 10, 11, 13, 11, 12, 27, 11, 25, 19, 15, 12, 11, 11, 16, 11, 11,
     21, 12, 0, 14, 9, 8, 21, 25, 32, 15, 11, 12, 10, 11, 15, 14, 8, 9, 19, 13, 12, 10, 11],
    [20, 14, 21, 17, 9, 18, 15, 26, 23, 24, 16, 21, 19, 21, 14, 14, 13, 13, 21, 10, 27, 7, 17, 41, 21, 12, 12, 12, 12,
     21, 13, 14, 0, 21, 13, 9, 6, 17, 8, 18, 7, 9, 10, 12, 12, 5, 14, 12, 12, 13, 11, 19],
    [18, 7, 16, 10, 23, 11, 13, 16, 21, 21, 12, 17, 28, 22, 22, 16, 16, 18, 31, 7, 18, 12, 21, 9, 31, 16, 11, 6, 9, 17,
     16, 9, 21, 0, 11, 13, 4, 9, 8, 15, 11, 12, 14, 11, 12, 18, 17, 11, 12, 14, 11, 12],
    [27, 14, 15, 15, 21, 21, 19, 8, 35, 36, 6, 24, 14, 31, 31, 12, 11, 9, 22, 14, 21, 14, 11, 7, 12, 12, 14, 10, 10, 14,
     9, 8, 13, 11, 0, 12, 10, 9, 4, 13, 11, 18, 25, 28, 29, 12, 11, 16, 18, 12, 10, 9],
    [18, 12, 19, 18, 22, 27, 21, 11, 21, 22, 10, 16, 18, 26, 29, 21, 16, 21, 20, 17, 21, 16, 14, 10, 16, 17, 11, 21, 11,
     21, 7, 21, 9, 13, 12, 0, 11, 8, 9, 16, 11, 10, 10, 11, 17, 16, 12, 7, 9, 14, 11, 7],
    [21, 18, 29, 27, 14, 11, 22, 15, 22, 16, 32, 13, 14, 28, 21, 41, 10, 8, 21, 11, 18, 12, 12, 11, 11, 12, 19, 19, 12,
     18, 11, 25, 6, 4, 10, 11, 0, 12, 8, 9, 13, 11, 5, 11, 12, 11, 16, 9, 10, 13, 7, 14],
    [12, 19, 31, 23, 17, 29, 18, 24, 31, 7, 21, 20, 16, 23, 13, 22, 9, 12, 24, 19, 14, 11, 11, 15, 17, 21, 21, 8, 17,
     11, 10, 32, 17, 9, 9, 8, 12, 0, 9, 11, 15, 22, 26, 21, 18, 12, 17, 16, 11, 12, 14, 11],
    [9, 11, 16, 20, 13, 22, 13, 29, 29, 15, 19, 28, 15, 16, 15, 12, 17, 18, 25, 21, 8, 17, 26, 26, 12, 12, 14, 15, 9,
     17, 7, 15, 8, 8, 4, 9, 8, 9, 0, 13, 18, 14, 11, 18, 13, 12, 16, 18, 15, 13, 11, 15],
    [15, 21, 19, 16, 11, 12, 16, 21, 21, 13, 16, 21, 19, 14, 18, 12, 14, 7, 12, 11, 11, 23, 28, 21, 9, 14, 11, 14, 4,
     13, 13, 11, 18, 15, 13, 16, 9, 11, 13, 0, 10, 17, 11, 13, 6, 9, 16, 11, 12, 11, 21, 24],
    [11, 20, 11, 14, 14, 17, 12, 20, 17, 6, 11, 26, 16, 13, 11, 33, 15, 27, 17, 13, 9, 21, 22, 24, 7, 19, 19, 12, 15,
     15, 11, 12, 7, 11, 11, 11, 13, 15, 18, 10, 0, 11, 5, 18, 9, 6, 12, 10, 9, 8, 11, 27],
    [21, 15, 21, 19, 18, 8, 13, 16, 13, 17, 32, 21, 13, 10, 12, 11, 12, 21, 14, 18, 11, 25, 12, 15, 10, 12, 7, 10, 17,
     11, 25, 10, 9, 12, 18, 10, 11, 22, 14, 17, 11, 0, 11, 15, 12, 25, 18, 13, 12, 16, 11, 12],
    [23, 13, 20, 11, 24, 11, 19, 11, 8, 14, 21, 15, 16, 7, 17, 9, 21, 16, 6, 21, 8, 28, 11, 8, 9, 18, 9, 17, 15, 27, 11,
     11, 10, 14, 25, 10, 5, 26, 11, 11, 5, 11, 0, 14, 15, 11, 8, 10, 8, 9, 11, 26],
    [18, 18, 24, 13, 28, 21, 21, 9, 16, 8, 18, 19, 17, 13, 14, 14, 12, 13, 9, 22, 11, 31, 26, 12, 21, 11, 12, 9, 19, 10,
     11, 15, 12, 11, 28, 11, 11, 21, 18, 13, 18, 15, 0, 0, 19, 11, 21, 9, 24, 11, 14, 11],
    [16, 14, 19, 22, 29, 30, 22, 24, 15, 15, 14, 11, 13, 16, 12, 12, 16, 11, 18, 13, 14, 26, 13, 9, 14, 15, 15, 17, 11,
     11, 15, 14, 12, 12, 29, 17, 12, 18, 13, 6, 9, 12, 0, 19, 0, 21, 6, 9, 11, 14, 8, 10],
    [31, 29, 21, 21, 30, 12, 17, 22, 7, 17, 12, 12, 18, 13, 6, 12, 16, 21, 11, 14, 10, 13, 11, 13, 11, 14, 31, 12, 10,
     12, 9, 8, 5, 18, 12, 16, 11, 12, 12, 9, 6, 25, 0, 11, 21, 0, 9, 7, 8, 13, 11, 21],
    [23, 21, 22, 21, 21, 16, 21, 15, 21, 12, 14, 17, 11, 20, 11, 15, 14, 25, 15, 17, 12, 12, 11, 16, 13, 21, 21, 14, 9,
     16, 7, 9, 14, 17, 11, 12, 16, 17, 16, 16, 12, 18, 0, 21, 6, 9, 0, 11, 14, 7, 9, 22],
    [26, 17, 27, 30, 25, 29, 21, 18, 9, 11, 13, 21, 16, 25, 12, 13, 13, 28, 12, 11, 14, 16, 23, 12, 11, 18, 11, 16, 15,
     14, 19, 19, 12, 11, 16, 7, 9, 16, 18, 11, 10, 13, 0, 9, 9, 7, 11, 0, 9, 14, 12, 12],
    [21, 24, 29, 19, 16, 22, 29, 13, 15, 21, 8, 22, 19, 17, 23, 12, 15, 21, 17, 18, 11, 17, 8, 24, 21, 16, 21, 12, 16,
     11, 8, 13, 12, 12, 18, 9, 10, 11, 15, 12, 9, 12, 0, 24, 11, 8, 14, 9, 0, 5, 15, 10],
    [20, 21, 33, 27, 11, 11, 24, 16, 12, 27, 11, 11, 24, 25, 8, 14, 9, 13, 11, 10, 21, 12, 7, 11, 11, 12, 15, 17, 17,
     12, 6, 12, 13, 14, 12, 14, 13, 12, 13, 11, 8, 16, 0, 11, 14, 13, 7, 14, 5, 0, 14, 7],
    [12, 19, 16, 25, 17, 15, 19, 13, 22, 23, 23, 9, 28, 22, 4, 19, 5, 8, 12, 21, 9, 12, 19, 21, 10, 7, 17, 11, 15, 9,
     10, 10, 11, 11, 10, 11, 7, 14, 11, 21, 11, 11, 0, 14, 8, 11, 9, 12, 15, 14, 0, 6],
    [100, 31, 21, 14, 24, 19, 11, 16, 21, 20, 14, 17, 31, 13, 11, 21, 11, 10, 7, 11, 21, 11, 9, 27, 8, 12, 14, 22, 12,
     8, 12, 11, 19, 12, 9, 7, 14, 11, 15, 24, 27, 12, 0, 11, 10, 21, 22, 12, 10, 7, 6, 0]]

service_time_in = [[0, 150],
                   [25, 40],
                   [145, 160],
                   [20, 35],
                   [410, 430],
                   [55, 70],
                   [375, 390],
                   [60, 85],
                   [45, 55],
                   [220, 235],
                   [95, 110],
                   [120, 130],
                   [70, 90],
                   [65, 80],
                   [410, 430],
                   [155, 160],
                   [190, 210],
                   [120, 130],
                   [360, 380],
                   [190, 220],
                   [165, 190],
                   [180, 200],
                   [140, 160],
                   [250, 280],
                   [220, 235],
                   [200, 215],
                   [230, 245],
                   [280, 300],
                   [240, 265],
                   [270, 290],
                   [300, 325],
                   [370, 395],
                   [340, 365],
                   [300, 315],
                   [300, 320],
                   [270, 295],
                   [240, 260],
                   [180, 195],
                   [310, 335],
                   [210, 235],
                   [360, 375],
                   [225, 240],
                   [85, 100],
                   [190, 220],
                   [385, 400],
                   [420, 433],
                   [470, 480],
                   [440, 460],
                   [245, 270],
                   [165, 190],
                   [480, 500],
                   [0, 720]]

pickup_delivery_time_in = [[0, 0, 0],
                           [2, 1, 1],
                           [2, 1, 1],
                           [2, 2, 2],
                           [4, 3, 3],
                           [2, 2, 2],
                           [3, 2, 2],
                           [4, 3, 3],
                           [4, 3, 3],
                           [3, 2, 2],
                           [3, 2, 2],
                           [3, 3, 3],
                           [4, 2, 2],
                           [3, 2, 2],
                           [2, 3, 3],
                           [3, 3, 3],
                           [3, 2, 2],
                           [2, 3, 3],
                           [4, 4, 4],
                           [3, 3, 3],
                           [3, 2, 2],
                           [2, 1, 1],
                           [4, 3, 3],
                           [5, 2, 2],
                           [3, 3, 3],
                           [4, 2, 2],
                           [5, 3, 3],
                           [3, 2, 2],
                           [4, 3, 3],
                           [4, 2, 2],
                           [5, 2, 2],
                           [3, 2, 2],
                           [3, 3, 3],
                           [2, 3, 3],
                           [4, 4, 4],
                           [5, 3, 3],
                           [4, 2, 2],
                           [5, 3, 3],
                           [4, 3, 3],
                           [6, 5, 5],
                           [4, 3, 3],
                           [6, 4, 4],
                           [3, 3, 3],
                           [5, 2, 2],
                           [6, 3, 3],
                           [4, 2, 2],
                           [3, 2, 2],
                           [2, 2, 2],
                           [4, 3, 3],
                           [3, 2, 2],
                           [2, 2, 2],
                           [0, 0, 0]]

number_of_vehicle: int = 8
number_of_cities: int = 20
tabu_itrs: int = 1000
aspiration: int = 100
start_node = 0
retention: int = 7
end_node: int = len(distance_mtrx) - 1
unserviced: list[int] = list(range(1, end_node + 1))
tabu_list: list[list[int]] = []
logging = False
grid_size: int = 99


# -------------------------------------------create random point---------------------------------------------------------------------------
def random_city() -> list:
    '''
    Generate a random list of cities with coordinates.

    :return coordinates_cities: List of the coordinates of the cities.
    '''
    coordinates_cities = {0: [0, 0]}
    for i in range(1, number_of_cities + 1):
        coordinates_cities[i] = [random.randint(
            -grid_size, grid_size), random.randint(-grid_size, grid_size)]
    coordinates_cities[number_of_cities + 1] = [0, 0]
    print(coordinates_cities)
    return coordinates_cities


def adj_matrix_generator(coordinates_cities: dict) -> dict:
    '''
    Generate the adjacency matrix of the cities.

    :param coordinates_cities: List of the coordinates of the cities.
    :return adj_matrix: Adjacency matrix of the cities.
    '''
    b = np.random.choice((True, False), size=(
        number_of_cities + 2, number_of_cities + 2), p=[0.6, 0.4])
    b_symm = np.logical_or(b, b.T)

    matrix = b_symm.astype(int)
    for i in range(len(matrix)):
        if(matrix[i][i] == 1):
            matrix[i][i] = 0

    print(matrix)
    return matrix

def distance_matrix_generator(matrix: list[list], coordinates_cities: dict) -> list:
    '''
    Generate the distance matrix of the cities.

    :param matrix: Adjacency matrix of the cities.
    :param coordinates_cities: List of the coordinates of the cities.
    :return distance_matrix: Distance matrix of the cities.
    '''
    distance_matrix = []
    for i in range(number_of_cities + 2):
        distance_matrix_line = []
        for j in range(number_of_cities + 2):
            if matrix[i][j] == 1:
                distance_matrix_line.append(math.sqrt((coordinates_cities[i][0] - coordinates_cities[j][0]) ** 2 + (
                    coordinates_cities[i][1] - coordinates_cities[j][1]) ** 2))
            else:
                distance_matrix_line.append(0)
        distance_matrix.append(distance_matrix_line)
    print(distance_matrix)
    return distance_matrix


def remove_us(c):
    if c != end_node and c in unserviced:
        unserviced.remove(c)


def get_cost(p_previous: int, p_next: int, p_service_start_time_previous: int, p_is_delayed_previous: bool) -> tuple[int, int, int, float, int, bool]:
    '''
    Calculates cost for travelling to one node to other node.

    :param p_previous: previous node number -- if travelling from node 2 to node 5 then prev = 2
    :param p_next: next node(customer)  -- if travelling from node 2 to node 5 then c = 5
    :param p_service_start_time_previous: service start time for previous node
    :param p_is_delayed_previous: boolean -- True if there is delay reaching to previous customer false otherwise

    :returns:
        :return distance_traveled: distance travelled
        :return wait_time: waiting time
        :return delay_time: delay time
        :return (wait_time / 4) + (delay_time / 4) + (distance_traveled): cost which needs to be minimized by greedy and tabu search
        :return service_start_time: service start time
        :return is_delayed: is delayed
    '''
    distance_traveled: int = distance_mtrx[p_previous][p_next]
    # Time to make a service at previous node
    pickup_delivery = sum(
        pickup_delivery_time_in[p_previous]) if not p_is_delayed_previous else 0
    # Time to make a service at next node, check if it has time to make a service before closing of the time window (service_time_in[p_next][1])
    delay_time = p_service_start_time_previous + pickup_delivery + distance_traveled - \
        service_time_in[p_next][1] if p_service_start_time_previous + pickup_delivery + \
        distance_traveled - service_time_in[p_next][1] > 0 else 0
    # Time to wait at next node
    wait_time = service_time_in[p_next][0] - p_service_start_time_previous - pickup_delivery - \
        distance_traveled if service_time_in[p_next][0] - \
        p_service_start_time_previous - pickup_delivery - distance_traveled > 0 else 0
    # Arrival time at next node
    service_start_time = p_service_start_time_previous + \
        pickup_delivery + distance_traveled + wait_time
    is_delayed = True if delay_time > 0 else False
    return distance_traveled, wait_time, delay_time, (wait_time / 4) + (delay_time / 4) + (distance_traveled), service_start_time, is_delayed


def get_initial_solution() -> list[list[int]]:
    '''
    Greedy algorithm to find initial solution.

    :return: solution with route in 2D array like solution : [[route-1][route-2].....] 
    '''
    list_routes: list[list[int]] = []
    compt_vehicle: int = 1
    startTime_prev: int = 0
    is_delayed_previous: bool = False
    bnode: int = 0
    while compt_vehicle in range(1, number_of_vehicle + 1):
        previous = 0
        route = [0]
        while not previous == end_node:
            minim = np.Infinity
            for next in unserviced:
                if previous == end_node:
                    break
                if previous == 0 and next == end_node:
                    continue
                if compt_vehicle == number_of_vehicle and len(unserviced) > 1 and next == end_node:
                    continue
                distance_traveled, wait_time, delay_time, cost, service_start_time, is_delayed = get_cost(
                    previous, next, startTime_prev, is_delayed_previous)
                if cost < minim:
                    bnode = next
                    minim = cost
                    startTime_prev = service_start_time
                    is_delayed_previous = is_delayed
            route.append(bnode)
            previous = bnode
            remove_us(bnode)
        list_routes.append(route)
        compt_vehicle += 1
    return list_routes


def get_exchange_neighbour(p_soln: list[list[int]]) -> list[list[int]] | int:
    '''
    Following function takes solution as input and returns the neighbouring solution by exchanging one node from a solution 
    to one node from other solution.

    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :return: neighbouring solution or sorted with cost in ascending order -1 if no neighbouring solution is found
    '''
    neighbours = []
    for combo in list(combinations(p_soln, 2)):
        for node1 in combo[0][:-1]:
            for node2 in combo[1][:-1]:
                if node1 == 0 or node2 == 0:
                    continue
                copy_sln = copy.deepcopy(p_soln)
                copy_combo1 = copy.deepcopy(combo[0])
                copy_combo2 = copy.deepcopy(combo[1])
                idx1 = copy_sln.index(copy_combo1)
                idx2 = copy_sln.index(copy_combo2)
                # Exchange node1 from combo1 to node2 from combo2
                copy_combo2.insert(copy_combo2.index(node2), node1)
                copy_combo1.insert(copy_combo1.index(node1), node2)
                copy_combo2.remove(node2)
                copy_combo1.remove(node1)
                copy_sln[idx1] = copy_combo1
                copy_sln[idx2] = copy_combo2
                # Check if solution is valid and more optimal than current solution
                if is_move_allowed((node2, node1, idx1, idx2), p_soln, copy_sln, 3):
                    neighbours.append((copy_sln, get_solution_actual_cost(
                        copy_sln), (3, node2, node1, idx2, idx1, retention)))
                    print_log('exchanging {0} from {1} to {2} from {3} resulting solution {4}'.format(node2, p_soln[idx2], node1,
                                                                                                      p_soln[idx1], copy_sln))

        for node1 in combo[1][:-1]:
            for node2 in combo[0][:-1]:
                if node1 == 0 or node2 == 0:
                    continue
                copy_sln = copy.deepcopy(p_soln)
                copy_combo1 = copy.deepcopy(combo[1])
                copy_combo2 = copy.deepcopy(combo[0])
                idx1 = copy_sln.index(copy_combo1)
                idx2 = copy_sln.index(copy_combo2)
                copy_combo2.insert(copy_combo2.index(node2), node1)
                copy_combo1.insert(copy_combo1.index(node1), node2)
                copy_combo2.remove(node2)
                copy_combo1.remove(node1)
                copy_sln[idx1] = copy_combo1
                copy_sln[idx2] = copy_combo2
                if is_move_allowed((node2, node1, idx1, idx2), p_soln, copy_sln, 3):
                    neighbours.append((copy_sln, get_solution_actual_cost(
                        copy_sln), (3, node2, node1, idx2, idx1, retention)))
                    print_log('exchanging {0} from {1} to {2} from {3} resulting solution {4}'.format(node2, p_soln[idx2], node1,
                                                                                                      p_soln[idx1], copy_sln))

    # print("{0} number of Neighbours after Exchange {1}".format(len(neighbours), neighbours))
    neighbours.sort(key=lambda x: x[1][-1])
    print_log("{0} number of sorted Neighbours after exchange {1}".format(
        len(neighbours), neighbours))
    return neighbours[0] if len(neighbours) > 0 else -1


def get_relocate_neighbour(p_soln: list[list[int]]) -> list[list[int]] | int:
    '''
    Following function takes solution as input and returns the neighbouring solution by relocating one node from a solution 
    in to other solution

    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :return: neighbouring solution or sorted with cost in ascending order -1 if no neighbouring solution is found
    '''
    neighbours = []
    for combo in list(combinations(p_soln, 2)):
        for i in combo[0][:-1]:  # -1 par rapport à la taille de la liste
            for j in combo[1][:-1]:
                if j == 0:  # On reviens pas au départ
                    continue
                copy_sln = copy.deepcopy(p_soln)
                copy_combo1 = copy.deepcopy(combo[0])
                copy_combo2 = copy.deepcopy(combo[1])
                idx1 = copy_sln.index(copy_combo1)
                idx2 = copy_sln.index(copy_combo2)
                # Relocate node1 from combo1 to node2 from combo2
                copy_combo2.remove(j)
                copy_combo1.insert(copy_combo1.index(i) + 1, j)
                copy_sln[idx1] = copy_combo1
                copy_sln[idx2] = copy_combo2
                if is_move_allowed((j, i, idx1, idx2), p_soln, copy_sln, 1):
                    print_log('relocating {0} from {1} to {2} after {3} resulting solution {4}'.format(j, p_soln[idx2],
                                                                                                       p_soln[idx1], i,
                                                                                                       copy_sln))
                    neighbours.append((copy_sln, get_solution_actual_cost(
                        copy_sln), (1, j, i, idx2, idx1, retention)))

        for i in combo[1][:-1]:
            for j in combo[0][:-1]:
                if j == 0:
                    continue
                copy_sln = copy.deepcopy(p_soln)
                copy_combo1 = copy.deepcopy(combo[1])
                copy_combo2 = copy.deepcopy(combo[0])
                idx1 = copy_sln.index(copy_combo1)
                idx2 = copy_sln.index(copy_combo2)
                copy_combo2.remove(j)
                copy_combo1.insert(copy_combo1.index(i) + 1, j)
                copy_sln[idx1] = copy_combo1
                copy_sln[idx2] = copy_combo2
                if is_move_allowed((j, i, idx1, idx2), p_soln, copy_sln, 1):
                    neighbours.append((copy_sln, get_solution_actual_cost(
                        copy_sln), (1, j, i, idx2, idx1, retention)))
                    print_log('relocating {0} from {1} to {2} after {3} resulting solution {4}'.format(j, p_soln[idx2],
                                                                                                       p_soln[idx1], i,
                                                                                                       copy_sln))

    # print("{0} number of Neighbours after relocation {1}".format(len(neighbours), neighbours))
    neighbours.sort(key=lambda x: x[1][-1])
    print_log("{0} number of sorted Neighbours after relocation {1}".format(
        len(neighbours), neighbours))
    return neighbours[0]


def get_shuffle_neighbours(p_soln: list[list[int]]) -> list[list[int]] | int:
    '''
    Following function takes solution as input and returns the neighbouring solution by shuffling nodes within a route with each other

    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :return: neighbouring solution or sorted with cost in ascending order -1 if no neighbouring solution is found
    '''
    neighbours = []
    for r in p_soln:
        for i in r[1:-1]:
            for j in r[1:-1]:
                copy_sln = copy.deepcopy(p_soln)
                _r = copy.deepcopy(r)
                idx = copy_sln.index(r)
                if i == j:
                    continue
                tmp = j
                idxi = r.index(i)
                _r[r.index(j)] = i
                _r[idxi] = j
                copy_sln[idx] = _r
                if is_move_allowed((j, i, idx, idx), p_soln, copy_sln, 2):
                    neighbours.append((copy_sln, get_solution_actual_cost(
                        copy_sln), (2, j, i, idx, idx, retention)))
                    print_log("changing position of {0} with {1} in route {2} resulting {3}".format(
                        i, j, r, _r))
    neighbours.sort(key=lambda x: x[1][-1])
    print_log("{0} number of sorted Neighbours after shuffling {1}".format(
        len(neighbours), neighbours))
    return neighbours[0] if len(neighbours) > 0 else -1


def get_neighbours(p_operation_performed: int, p_soln: list[list[int]]) -> list[list[int]] | int:
    '''
    Following function takes solution as input and returns the neighbouring solution by exchanging nodes between two routes.

    :param op: operation to be performed
    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :return: neighbouring solution or sorted with cost in ascending order -1 if no neighbouring solution is found
    '''
    if p_operation_performed == 1:
        return get_relocate_neighbour(p_soln)
    elif p_operation_performed == 2:
        return get_shuffle_neighbours(p_soln)
    elif p_operation_performed == 3:
        return get_exchange_neighbour(p_soln)


def get_solution_cost(p_soln: list[list[int]]) -> tuple[float, float, float, float, int, int, list[list[float]]]:
    '''
    Calculate the cost for solution it uses the  get_cost function internally.

    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :returns:
        :return distance: total distance of the solution
        :return delay: total delay of the solution
        :return wait: total wait of the solution
        :return cost: total cost of the solution
        :return serviced: number of serviced customers
        :return unserviced: number of unserviced customers
        :return details: route details for route [(wait time,delay time,service start time)] each () have details for each
            customer and each row represents a route
    '''
    cost = 0
    wait = 0
    delay = 0
    serviced = 0
    unserviced = 0
    distance = 0
    details = []
    for route in p_soln:
        prev = 0
        prev_sst = 0
        details_tmp = []
        is_delayed = False
        for customer in route[1:]:
            d, w, dl, c, sst, isd = get_cost(
                prev, customer, prev_sst, is_delayed)
            prev_sst = sst
            is_delayed = isd
            prev = customer
            if isd:
                unserviced += 1
            else:
                serviced += 1
            distance += d
            delay += dl
            wait += w
            cost += c
            details_tmp.append((w, dl, sst))
        details.append(details_tmp)

    return distance, delay, wait, cost, serviced, unserviced, details


def get_solution_actual_cost(p_soln: list[list[int]]) -> tuple[float, float, float, float, int, int]:
    '''
    Calculate the cost for solution it uses the  get_cost function internally its same as above but 
    returns less parameters.

    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :returns:
        :return distance: total distance of the solution
        :return delay: total delay of the solution
        :return wait: total wait of the solution
        :return cost: total cost of the solution
    '''
    cost = 0
    wait = 0
    delay = 0
    serviced = 0
    unserviced = 0
    distance = 0
    details = []
    for route in p_soln:
        prev = 0
        prev_sst = 0
        details_tmp = []
        is_delayed = False
        for customer in route[1:]:
            d, w, dl, c, sst, isd = get_cost(
                prev, customer, prev_sst, is_delayed)
            # c = c + (dl * 39)
            prev_sst = sst
            is_delayed = isd
            prev = customer
            if isd:
                unserviced += 1
            else:
                serviced += 1
            distance += d
            delay += dl
            wait += w
            cost += c
            details_tmp.append((w, dl, sst))
        details.append(details_tmp)

    return distance, delay, wait, cost


def get_distance_for_solution(p_soln: list[list[int]]) -> float:
    '''
    Function is to find total distance for solution without pickup/delivery time

    :param soln: solution in 2D array like solution : [[route-1][route-2].....]
    :return: total distance of the solution
    '''
    d = 0
    distance = []
    for route in p_soln:
        prev = 0
        for customer in route[1:]:
            d += get_distance(prev, customer)
            prev = customer
        distance.append(d)
        d = 0
    return distance


def tabu_search(p_routes: list[list[int]], p_iterations: int) -> tuple[list[list[int]], float]:
    '''
    Tabu search driver method

    :param routes: routes in 2D array like solution : [[route-1][route-2].....]
    :param iterations: number of iterations to be performed
    :return (best_solution_ever, best_cost_ever): best solution and cost
    '''
    best_solution_ever = p_routes
    best_cost_ever = get_solution_actual_cost(p_routes)
    # Nombre de fois que la meilleure solution n'a pas changé
    best_solution_ever_not_chaned_itr_count = 0
    best_soln = p_routes
    best_cost = ()
    tmp12 = []
    global tabu_list
    for i in range(p_iterations - 1):
        tmp12 = []
        if best_solution_ever_not_chaned_itr_count > 7:
            break
        tmp12.append(get_neighbours(1, best_soln))
        tmp12.append(get_neighbours(3, best_soln))
        tmp11 = get_neighbours(2, best_soln)
        if not tmp11 == -1:
            tmp12.append(tmp11)
        tmp12.sort(key=lambda x: x[1][-1])
        if tmp12[1] == -1 or tmp12[0] == -1:
            break
        best_soln = tmp12[0][0]
        best_cost = tmp12[0][1]
        tabu_list.append(TabuListClass(
            tmp12[0][2][0], tmp12[0][2][1:-1], tmp12[0][2][-1]))

        if best_cost_ever[-1] > best_cost[-1]:  # Wait time
            best_cost_ever = best_cost
            best_solution_ever = best_soln
        else:
            best_solution_ever_not_chaned_itr_count += 1
        print("best solution so far {0}".format(best_soln))
        iteration_update_tabu_list()
    tabu_list = []
    return best_solution_ever, best_cost_ever


# ------------- input provider methods-----------------------------------------------------------------
def get_distance(p_src: int, p_dest: int) -> float:
    '''
    Function to get distance between two customers

    :param src: source customer
    :param dest: destination customer
    :return: distance between two customers
    '''
    return distance_mtrx[p_src][p_dest]


def get_pickup_time(p_cust: int) -> int:
    '''
    Function to get pickup time for a customer

    :param cust: customer
    :return: pickup time for a customer
    '''
    return pickup_delivery_time_in[p_cust][0]


def get_latest_service_time(p_cust: int) -> int:
    '''
    Function to get latest service time for a customer

    :param cust: customer
    :return: latest service time for a customer
    '''
    return service_time_in[p_cust][1]


def is_empty_route(p_route: list[int]) -> bool:
    '''
    Function to check if a route is empty

    :param route: route
    :return: True if route is empty else False
    '''
    if len(p_route) == 2 and 0 in p_route and len(distance_mtrx) - 1 in p_route:
        return True
    return False


def contains(p_list: list[list[int]], p_filter) -> bool:
    '''
    Function to check if a list contains a filter

    :param list: list of elements
    :param filter: filter
    :return: True if list contains filter else False
    '''
    for x in p_list:
        if p_filter(x):
            return True
    return False

# -----------------end ---------input provider methods---------------------------------------------------------


class TabuListClass:
    '''
    Class to store tabu list

    :attr op: operation performed on the tabu list
    :attr route: route on which operation was performed
    :attr valid_for: number of iterations for which the tabu list is valid
    '''

    def __init__(self, p_op: int, p_move: list[int], p_valid_for: int):
        self.op = p_op
        self.move = p_move
        self.valid_for = p_valid_for

    def checked(self):
        if self.valid_for > 0:
            self.valid_for -= 1
            return self.valid_for
        else:
            return -1

    def find(self, p_move: list[int], p_aspired: bool, p_op: int):
        if self.op == p_op and self.move == p_move and self.valid_for > 0 and not p_aspired:
            print("found tabu match op : {0} move : {1}".format(
                self.op, self.move))
            return True
        return False


'''
to check current move against tabu list if not available in tabu list then move is allowed otherwise not allowed
function also check for aspiration criteria
'''


def is_move_allowed(p_move: tuple[int, int, int, int], p_soln_prev: list[list[int]], p_soln_curr: list[list[int]], p_operation_performed: int) -> bool:
    '''
    To check current move against tabu list if not available in tabu list then move is allowed otherwise not allowed 
    function also check for aspiration criteria

    :param move: Exchanged nodes and their positions
    :param soln_prev: Previous solution
    :param soln_curr: Current solution
    :param op: Operation performed
    :return: True if move is allowed else False
    '''
    if len(tabu_list) < 1:
        return True
    cost_prev = get_solution_actual_cost(p_soln_prev)[-1]
    cost_curr = get_solution_actual_cost(p_soln_curr)[-1]
    if cost_prev - cost_curr > aspiration:
        return not contains(tabu_list, lambda x: x.find(p_move, True, p_operation_performed))
    else:
        return not contains(tabu_list, lambda x: x.find(p_move, False, p_operation_performed))


def iteration_update_tabu_list() -> None:
    '''
    To update tabu list iteration wise.
    '''
    for i in tabu_list:
        if i.checked() < 0:
            tabu_list.remove(i)


# utility function to print 2d array linewise rows
def print2D(arr: list[list[int]]) -> None:
    '''
    To print 2d array linewise rows

    :param arr: 2d array
    '''
    for row in arr:
        print(row)


# log utility method
def print_log(log: str) -> None:
    '''
    To print log

    :param log: log
    '''
    if logging:
        print(log)


# log = open("myprog.log", "a")
# sys.stdout = log

# Generate distance matrix
list_cities = random_city()
matrice = adj_matrix_generator(list_cities)
distance_mtrx = distance_matrix_generator(matrice, list_cities)
end_node = len(distance_mtrx) - 1
unserviced = list(range(1, end_node + 1))

# Launch the algorithm
routes = get_initial_solution()
print("Best solution: {0}".format(routes))
# routes.remove([])
best_soln, best_cost = tabu_search(routes, tabu_itrs)
print("solution is : {0} with costs : {1}".format(best_soln, best_cost))
best_cost = get_solution_actual_cost(best_soln)
index1 = 0

plt.title("Best solution for VRPTW")

print(list_cities)
for index1, route in enumerate(best_soln):
    print("Route{0} is: {1}".format(index1, route))
    x = [0]
    y = [0]
    plt.scatter(x, y)
    for point in route:
        x.append(list_cities[point][0])
        y.append(list_cities[point][1])
    x.append(0)
    y.append(0)
    plt.plot(x, y, label="Camion {0}".format(index1))
    # plt.pause(0.5)  # pause for 0.5 second
plt.legend()
plt.show()

distance, delay, wait, cost, serviced, unserviced, details = get_solution_cost(
    best_soln)

print("total distance: {0}".format(distance))
print("total waiting: {0}".format(wait))
print("total delay: {0}".format(delay))
print("total cost: {0}".format(cost))
print("Total serviced customers: {0}".format(serviced - index1))
print("Total unserviced customers: {0}".format(unserviced))
print("route wise Distance without pickup /delivery is {0}".format(
    get_distance_for_solution(best_soln)))

print("Below is the route details for route [(wait time,delay time,service start time)] each () have details for each "
      "customer and each row represents a route")
print2D(details)
