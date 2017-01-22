#!ipython
# -*- coding:utf-8 -*-

import numpy as np


def harr(arr):

    def harr_solve(arr):
        a = arr[::2]
        b = arr[1::2]
        if len(a) > len(b):
            b0 = np.zeros(len(a), dtype=a.dtype)
            b0[:-1] = b
            b = b0
        phai = (a + b)/2
        psai = (a - b)/2
        return phai, psai
    w = False
    p = arr
    s = []
    while not w:
        p, s_ = harr_solve(p)
        # print(p)
        s.insert(0, s_)
        if len(p) == 1:
            w = True
    return p, s


def iharr(base, wavelet, length=None):

    def iharr_join(phai, psai):
        p = np.zeros(2*len(psai), dtype=psai.dtype)
        if len(phai) > len(psai):
            phai = phai[:-1]
        a = phai + psai
        b = phai - psai
        p[::2] = a
        p[1::2] = b
        return p

    for i in wavelet:
        base = iharr_join(base, i)
    if length is not None and length < len(base):
        base = base[:-1]
    return base
