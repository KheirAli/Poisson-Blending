#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 13:47:51 2022

@author: alirezakheirandish
"""


import numpy as np
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt


source = plt.imread("res05.png")
source = source[:,:,0:3]

target = plt.imread("res06.png")
target = target[:,:,0:3]

# source[0,0],target[0,0]

source = np.round(255*source)
source = np.asarray(source,dtype = np.uint8)
target = np.round(255*target)
target = np.asarray(target,dtype = np.uint8)

# plt.imshow(source)

source = source[200:270,30:160,:]
# plt.imshow(source)

# plt.imshow(target)

mask = np.ones((source.shape[0],source.shape[1]), dtype=np.uint8)
mask[:10,:] = 0
mask[-10:,:] = 0
mask[:,:10] = 0
mask[:,-10:] = 0

D = {}
counter = 0

offset = [260, 100]         #place the bird every place you want by setting offset

for i in range(mask.shape[0]):
    for j in range(mask.shape[1]):
        if mask[i][j] == 1:
            D[(i+offset[0], j+offset[1])] = counter
            counter += 1
copy_source = np.zeros(target.shape, dtype=int)
copy_source[offset[0]:source.shape[0]+offset[0],offset[1]:source.shape[1]+offset[1],:] = source[:,:,:]

# plt.imshow(np.uint8(copy_paste))
A = np.zeros((len(D),len(D)), dtype=int)
b = np.zeros((len(D),3), dtype=int)

# copy_paste[offset[0],offset[1]],source[0,0]

for k, v in D.items():
        A[v][v] = 4
#         TEST = 4*target[k[0]][k[1]] - target[k[0]+1][k[1]]- target[k[0]-1][k[1]] - target[k[0]][k[1]+1] - target[k[0]][k[1]-1]
        TEST1 = 4*copy_source[k[0]][k[1]] - copy_source[k[0]+1][k[1]]- copy_source[k[0]-1][k[1]] - copy_source[k[0]][k[1]+1] - copy_source[k[0]][k[1]-1]
#         if np.mean(abs(TEST))>np.mean(abs(TEST1)):
#             A[v][v] = 40
#             b[v] += 40*target[k[0]][k[1]]
#         else:
        b[v] += TEST1   
#         zarf = 0
#         counter = 0
        if (k[0]+1, k[1]) in D:
            A[v][D[(k[0]+1, k[1])]] = -1
#             counter += 1
        else:
            b[v] += target[k[0]+1][k[1]]
            

        if (k[0]-1, k[1]) in D:
            A[v][D[(k[0]-1, k[1])]] = -1
        else:
            b[v] += target[k[0]-1][k[1]]

        if (k[0], k[1]+1) in D:
            A[v][D[(k[0], k[1]+1)]] = -1
        else:
            b[v] += target[k[0]][k[1]+1]

        if (k[0], k[1]-1) in D:
            A[v][D[(k[0], k[1]-1)]] = -1
        else:
            b[v] += target[k[0]][k[1]-1]



x = spsolve(A, b)

for k, v in D.items():
    for i in range(3):
        if x[v][i]>255:
            target[k[0]][k[1]][i] = np.uint8(255)
        elif x[v][i]<0:
            target[k[0]][k[1]][i] = np.uint8(0)
        else:
            target[k[0]][k[1]][i] = np.uint8((x[v][i]))

plt.imsave("result_231.jpg", target)