#!ipython
# -*- coding:utf-8 -*-

# from PIL import Image
import numpy as np
from npcolorconvert import npjch2rgb, nprgb2jch
from functools import reduce
# import matplotlib.pyplot as plt
from fftim import *


def gaussian_blur_array(array, radius):
    arr_map = []
    for i in range(radius*2 + 1):
        for j in range(radius * 2 + 1):
            i_ = i - radius
            j_ = j - radius
            a = np.roll(np.roll(array, i_, axis=0), j_, axis=1)
            arr_map.append(a)
    return reduce(lambda x, y: x+y, arr_map) / ((radius * 2 + 1) ** 2)


def gaussian_blur_im(im, radius):
    rgb = np.array(im)
    jch = nprgb2jch(rgb)
    jch[:, :, 0] = gaussian_blur_array(jch[:, :, 0], radius)
    jch[:, :, 1] = gaussian_blur_array(jch[:, :, 1], radius)
    jch[:, :, 2] = gaussian_blur_array(jch[:, :, 2], radius)
    image = npjch2rgb(jch)
    return image


def masked_fftblur(im, seq1, seq2, radius, aparg):
    jchfft = image_2_fft(im)
    jch_mask = jchfft.copy()
    sap = shifted_fftarray_apply

    def func(x, y):
        return x * y

    for i in aparg:
        a = gaussian_blur_array(jch_mask[:, :, i], radius)
        b = sap(func, a, seq1, seq2)
        t = sap(func, jchfft[:, :, i], 1 - seq1, 1-seq2)

        jch_mask[:, :, i] = b + t
    im = fft_2_image(jch_mask)
    return im
