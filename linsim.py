#!ipython
# -*- coding:utf-8 -*-

# from PIL import Image, ImageDraw
import numpy as np
# from npcolorconvert import npjch2rgb, nprgb2jch
# import matplotlib.pyplot as plt
# import random
# import string


def num_sim(lis1, lis2, threshold=None, argwhere=False):
    if threshold is None:
        threshold = max(np.max(lis1)-np.min(lis1),
                        np.max(lis2)-np.min(lis2)) * 0.05
    diff_lis = lis1 - lis2
    s = np.abs(diff_lis - np.mean(diff_lis)) <= threshold
    if not argwhere:
        return np.sum(s) / len(diff_lis)
    else:
        return np.sum(s) / len(diff_lis), np.logical_not(s)


def prop_sim(lis1, lis2, threshold=None, argwhere=False):
    if threshold is None:
        threshold = max(np.max(lis1)-np.min(lis1),
                        np.max(lis2)-np.min(lis2)) * 0.05
    b1 = lis1 - np.mean(lis1)
    b2 = lis2 - np.mean(lis2)
    length = len(b1)
    p1 = np.sum(np.abs(b1)) / length
    p2 = np.sum(np.abs(b2)) / length
    if p1 > p2:
        threshold = threshold * p1
    else:
        threshold = threshold * p2
    l1 = b1 * p2
    l2 = b2 * p1
    diff_lis = l1 - l2
    s = np.abs(diff_lis - np.mean(diff_lis)) <= threshold
    if not argwhere:
        return np.sum(s) / length
    else:
        return np.sum(s) / length, np.logical_not(s)


def sign_sim(lis1, lis2, argwhere=False):
    delta1 = np.roll(lis1, -1) - lis1
    delta1[-1] = 0
    delta2 = np.roll(lis2, -1) - lis2
    delta2[-1] = 0
    sign1 = np.sign(delta1)
    sign2 = np.sign(delta2)
    s = sign1 == sign2
    if not argwhere:
        return np.sum(s) / len(s)
    else:
        return np.sum(s) / len(s), np.logical_not(s)


def d2_sim(lis1, lis2, threshold=0.01, argwhere=False):
    delta1 = np.roll(lis1, -1) - lis1
    delta1[-1] = 0
    delta2 = np.roll(lis2, -1) - lis2
    delta2[-1] = 0
    delrad1 = np.roll(delta1, -1) - delta1
    delrad1[-1] = 0
    delrad2 = np.roll(delta2, -1) - delta2
    delrad2[-1] = 0
    diff_lis = delrad1 - delrad2
    s = np.abs(diff_lis) <= threshold
    if not argwhere:
        return np.sum(s) / len(s)
    else:
        return np.sum(s) / len(s), np.logical_not(s)


def prop_differ(lis1, lis2, threshold=None):
    if threshold is None:
        threshold = max(np.max(lis1)-np.min(lis1),
                        np.max(lis2)-np.min(lis2)) * 0.05
    b1 = lis1 - np.mean(lis1)
    b2 = lis2 - np.mean(lis2)
    length = len(b1)
    p1 = np.sum(np.abs(b1)) / length
    p2 = np.sum(np.abs(b2)) / length
    # print(threshold, p1, p2)
    if p1 > p2:
        threshold = threshold * p1
    else:
        threshold = threshold * p2
    # print(threshold)
    l1 = b1 * p2
    l2 = b2 * p1
    return l1, l2
