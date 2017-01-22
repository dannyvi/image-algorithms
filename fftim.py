#!ipython
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw
import numpy as np
from npcolorconvert import npjch2rgb, nprgb2jch
from functools import reduce
import matplotlib.pyplot as plt
import random, string


def image_2_fft(image):
    rgb = np.array(image)
    jch = nprgb2jch(rgb.reshape(-1, 3)).reshape(rgb.shape)
    jchfft = np.zeros(jch.shape, dtype='complex')
    j = jch[:, :, 0]
    fftj = np.fft.fft2(j)
    sfftj = np.fft.fftshift(fftj)
    # sig =
    c = jch[:, :, 1]
    fftc = np.fft.fft2(c)
    sfftc = np.fft.fftshift(fftc)
    h = jch[:, :, 2]
    ffth = np.fft.fft2(h)
    sffth = np.fft.fftshift(ffth)
    jchfft[:, :, 0] = sfftj
    jchfft[:, :, 1] = sfftc
    jchfft[:, :, 2] = sffth
    return jchfft


def fft_2_image(jchfft):
    fftj = np.fft.ifftshift(jchfft[:, :, 0])
    j = np.fft.ifft2(fftj)
    fftc = np.fft.ifftshift(jchfft[:, :, 1])
    c = np.fft.ifft2(fftc)
    ffth = np.fft.ifftshift(jchfft[:, :, 2])
    h = np.fft.ifft2(ffth)
    jch = np.zeros(jchfft.shape)
    jch[:, :, 0] = j.real
    jch[:, :, 1] = c.real
    jch[:, :, 2] = np.fmod(h.real, 360)
    rgb = npjch2rgb(jch.reshape(-1, 3)).reshape(jch.shape)
    return Image.fromarray(rgb)


def fft_2_freq_angle(jchfft):
    freq = np.abs(jchfft)
    angle = np.angle(jchfft)
    return [freq, angle]


def freq_angle_2_fft(frq, angle):
    jchfft = np.multiply(frq, np.exp(1j*angle))
    return jchfft


def reshape_freq(freq):
    fq = np.log10(freq+1)
    coef = np.log(100) / np.log(np.max(fq))
    fqj = fq ** coef
    return fqj, coef


def reverse_freq(fqj, coef):
    fq = fqj ** (1 / coef)
    freq = np.power(10, fq) - 1
    return freq


def image_2_logfreq(im):
    jchfft = image_2_fft(im)
    freq, angle = fft_2_freq_angle(jchfft)
    fj = freq[:, :, 0]
    fc = freq[:, :, 1]
    fh = freq[:, :, 2]
    fqj, coefj = reshape_freq(fj)
    fqc, coefc = reshape_freq(fc)
    fqh, coefh = reshape_freq(fh)
    freq[:, :, 0] = fqj
    freq[:, :, 1] = fqc
    freq[:, :, 2] = fqh
    return [freq, angle, [coefj, coefc, coefh]]


def logfreq_2_image(fq, angle, coef):
    j = fq[:, :, 0]
    c = fq[:, :, 1]
    h = fq[:, :, 2]
    freqj = reverse_freq(j, coef[0])
    freqc = reverse_freq(c, coef[1])
    freqh = reverse_freq(h, coef[2])
    freq = np.zeros(fq.shape)
    freq[:, :, 0] = freqj
    freq[:, :, 1] = freqc
    freq[:, :, 2] = freqh
    jchfft = freq_angle_2_fft(freq, angle)
    image = fft_2_image(jchfft)
    return image


def show_array(array, title=None):
    jch = np.zeros(array.shape+(3,))
    jch[:, :, 0] = array
    rgb = npjch2rgb(jch.reshape(-1, 3)).reshape(jch.shape)
    im = Image.fromarray(rgb)
    im.show(title)


def show_image_jchfft(im, title=None):
    freq, angle, coef = image_2_logfreq(im)
    tail = ['-j', '-c', '-h']
    if title is not None:
        tail = [title+'-j', title+'-c', title+'-h']
    for i in range(3):
        show_array(freq[:, :, i], title=tail[i])


def shifted_fftarray_apply(func, arr, seq1, seq2):
    afseq1 = np.zeros(arr. shape[1], dtype=arr.dtype)
    afseq2 = np.zeros(arr. shape[0], dtype=arr.dtype)
    afseq1[:len(seq1)] = seq1
    afseq2[:len(seq2)] = seq2

    if len(afseq1) % 2 == 0:
        afseq1[len(seq1):] = seq1[::-1]
    else:
        afseq1[len(seq1):] = seq1[:0:-1]
    if len(afseq2) % 2 == 0:
        afseq2[len(seq2):] = seq2[::-1]
    else:
        afseq2[len(seq2):] = seq2[:0:-1]
    afseq1 = np.fft.fftshift(afseq1)
    afseq2 = (np.fft.fftshift(afseq2)).reshape(-1, 1)
    afseq = afseq1 * afseq2
    return func(arr, afseq)


def image_apply_seq(im, func, seq1, seq2, aparg):
    jchfft = image_2_fft(im)
    sap = shifted_fftarray_apply
    for i in aparg:
        jchfft[:, :, i] = sap(func, jchfft[:, :, i], seq1, seq2)
    im = fft_2_image(jchfft)
    return im


def get_apply_seq_length(im):
    seq1length = (im.size[0] + 1) // 2
    seq2length = (im.size[1] + 1) // 2
    return seq1length, seq2length
