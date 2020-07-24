#!/bin/env python

array = [list("lc3b"), list("?4Cd"), list("I}rC"), list("STm{")]

def transpose(v):
    return [[v[j][i] for j in range(len(v))] for i in range(len(v[0]))]

def rotate(v, k):
    k = k % len(v) #len(v)==4
    return v[k:] + v[:k]

transp = transpose(array)

for i in range(4):
    res1 = [[rotate(transp[k], i)] for k in range(4)]
    for j in range(4):
        transp2 = transpose(res1)
        res2 = rotate(transp2[0], j)
        print(res2)
