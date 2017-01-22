#!ipython
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw
import numpy as np
from npcolorconvert import npjch2rgb, nprgb2jch
import matplotlib.pyplot as plt
import random
import string


def show_jch_rgb(jch, rgb, figsize=(8, 6)):
    fig = plt.figure(figsize=figsize)
    w, h = figsize
    length = len(jch)
    xtick = np.arange(length)
    if length > 100:
        xtick = np.arange(length//(length//100))*(length//100)
    plt.subplots_adjust(0.5/w, 0.6/h, 1-0.3/w, 1-0.3/h, 0, 0.6/h)
    p1 = plt.subplot(211)
    p1.set_xticks(xtick)
    p1.set_xticklabels(xtick, rotation=-90)
    p1.grid(True)
    p1.plot(jch[:, 0], '|-', color=(0.1, 0.1, 0.1))
    p1.plot(jch[:, 1], '|-', color=(0.7, 0.7, 0.7))
    p1.plot(jch[:, 2], '|-', color=(0.6, 0.4, 0.8))
    p2 = plt.subplot(212)
    p2.set_xticks(xtick)
    p2.set_xticklabels(xtick, rotation=-90)
    p2.grid(True)
    p2.plot(rgb[:, 0], '|-', color=(0.6, 0.1, 0.1))
    p2.plot(rgb[:, 1], '|-', color=(0.1, 0.7, 0.2))
    p2.plot(rgb[:, 2], '|-', color=(0.1, 0.3, 0.7))
    filename = '/tmp/' + \
        ''.join(random.sample(string.ascii_letters+string.digits, 8))+'.png'
    plt.savefig(filename)
    plt.close()
    im = Image.open(filename)
    im.show()


def plot_jch_rgb(jch, rgb, figsize=(8, 6)):
    fig = plt.figure(figsize=figsize)
    w, h = figsize
    length = len(jch)
    xtick = np.arange(length)
    if length >= 100:
        xtick = np.arange(length//(length//100))*(length//100)
    plt.subplots_adjust(0.5/w, 0.6/h, 1-0.3/w, 1-0.3/h, 0, 0.6/h)
    p1 = plt.subplot(211)
    p1.set_xticks(xtick)
    p1.set_xticklabels(xtick, rotation=-90)
    p1.grid(True)
    p1.plot(jch[:, 0], '|-', color=(0.1, 0.1, 0.1))
    p1.plot(jch[:, 1], '|-', color=(0.7, 0.7, 0.7))
    p1.plot(jch[:, 2], '|-', color=(0.6, 0.4, 0.8))
    p2 = plt.subplot(212)
    p2.set_xticks(xtick)
    p2.set_xticklabels(xtick, rotation=-90)
    p2.grid(True)
    p2.plot(rgb[:, 0], '|-', color=(0.6, 0.1, 0.1))
    p2.plot(rgb[:, 1], '|-', color=(0.1, 0.7, 0.2))
    p2.plot(rgb[:, 2], '|-', color=(0.1, 0.3, 0.7))
    plt.show()
