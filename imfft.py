#!ipython
# -*- coding:utf-8 -*-

from PIL import Image
from npcolorconvert import npjch2rgb, nprgb2jch
import numpy as np
# from imagealgo import get_line,show_line,show_fftseq,apply_seq,view_instances
from fftim import *

# im1 = Image.open
# sample1 = get_line(Image.open('compare_1.jpg'),[100,500],30,300)
# ,['compare_1.jpg'])
# sample2 =
# get_line(Image.open('./chosen/DSC_8302.jpg'),[100,800],45,300)#,['./chosen/DSC_8302.jpg'])

sqrt2 = 1.4142135623730951


def increase_detail_1(im):
    l1, l2 = get_apply_seq_length(im)
    seq1 = np.linspace(1, sqrt2, l1)
    seq2 = np.linspace(1, sqrt2, l2)
    return image_apply_seq(im, lambda x, y: x * y, seq1, seq2, [0])


def increase_detail_2(im):
    l1, l2 = get_apply_seq_length(im)
    seq1 = np.linspace(1, sqrt2 ** 0.5, l1) ** 2
    seq2 = np.linspace(1, sqrt2 ** 0.5, l2) ** 2
    return image_apply_seq(im, lambda x, y: x * y, seq1, seq2, [0, 1])
