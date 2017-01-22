#!ipython
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw
import numpy as np
from npcolorconvert import npjch2rgb, nprgb2jch
import matplotlib.pyplot as plt
import random
import string


def rotate_2d(point, angle):
    a = angle * np.pi / 180
    x, y = point
    x_ = x * np.cos(a) + y * np.sin(a)
    y_ = y * np.cos(a) - x * np.sin(a)
    return [x_, y_]


def get_line(image, start_point, angle, length):
    center = [image.size[0] // 2, image.size[1] // 2]
    rel_point = [start_point[0] - center[0], start_point[1] - center[1]]
    trans_point = rotate_2d(rel_point, -angle)
    image_ = image.rotate(-angle, resample=Image.BILINEAR, expand=True)
    center2 = [image_.size[0] // 2, image_.size[1] // 2]
    start_p = [center2[0] + trans_point[0], center2[1] + trans_point[1]]
    # assert(start_p[0]>0 and start_p[0]<image_.size[0])
    assert(start_p[1] > 0 and start_p[1] < image. size[1])
    if start_p[0] < 0:
        length = length + start_p[0]
        start_p[0] = 0
    elif start_p[0] > image_.size[0]:
        start_p[0] = image_.size[0]-1
        length = 0
    if start_p[0] + length > image_.size[0]:
        length = image_.size[0] - start_p[0]
    rgblist = np.array(image_)[start_p[1], start_p[0]:start_p[0]+length]
    jchlist = nprgb2jch(rgblist)
    return jchlist, rgblist


def plot_line(linelist):
    clist = linelist  # jchlist[:,jcharg]
    flist = np.fft.fftshift(np.abs(np.fft.fft(clist)))
    alist = np.fft.fftshift(np.angle(np.fft.fft(clist)))
    freq = np.fft.fftshift(np.fft.fftfreq(len(clist)))
    length = len(clist)
    xtick = np.arange(length)
    if length > 30:
        xtick = np.arange(length//(length//30))*(length//30)
        freq = freq[::length//30]
    color = (0.6, 0.0, 0.1)
    p1 = plt.subplot(311)
    p1.set_title('origin')
    p1.plot(clist, color=color)
    p1.set_xticks(xtick)
    p1.set_xticklabels(xtick, rotation=-90)
    # p1.set_yticks(np.arange(100//10) * 10)
    p1.grid(True)
    p1.legend()
    p2 = plt.subplot(312)
    p2.plot(flist, color=color)
    p2.set_title('frequency')
    p2.set_xticks(xtick)
    p2.set_xticklabels(freq, rotation=-90)
    # p2.set_xticks(np.arange(length//(length//30)) * (length // 30),\
    #              freq[::length//30],rotation=-90)
    # p2.set_yticks(np.arange(100//10) * 10)
    p2.grid(True)
    p3 = plt.subplot(313)
    p3.plot(alist, color=color)
    p3.set_title('angle')
    p3.set_xticks(xtick)
    p3.set_xticklabels(freq, rotation=-90)
    p3.grid(True)
    return plt
    # plt.show()


def plot_fftseq(fftseq):
    flist = np.fft.fftshift(np.abs(fftseq))
    alist = np.fft.fftshift(np.angle(fftseq))
    clist = np.fft.ifft(fftseq)
    freq = np.fft.fftshift(np.fft.fftfreq(len(clist)))
    length = len(clist)
    xtick = np.arange(length)
    if length > 30:
        xtick = np.arange(length//(length//30))*(length//30)
        freq = freq[::length//30]
    color = (0.6, 0.0, 0.1)
    p1 = plt.subplot(311)
    p1.set_title('origin')
    p1.plot(clist, color=color)
    p1.set_xticks(xtick)
    p1.set_xticklabels(xtick, rotation=-90)
    # p1.set_yticks(np.arange(100//10) * 10)
    p1.grid(True)
    p1.legend()
    p2 = plt.subplot(312)
    p2.plot(flist, color=color)
    p2.set_title('frequency')
    p2.set_xticks(xtick)
    p2.set_xticklabels(freq, rotation=-90)
    # p2.set_xticks(np.arange(length//(length//30)) * (length // 30),\
    #              freq[::length//30],rotation=-90)
    # p2.set_yticks(np.arange(100//10) * 10)
    p2.grid(True)
    p3 = plt.subplot(313)
    p3.plot(alist, color=color)
    p3.set_title('angle')
    p3.set_xticks(xtick)
    p3.set_xticklabels(freq, rotation=-90)
    p3.grid(True)
    # plt.show()
    return plt


def present_line(line):
    p = plot_line(line)
    p.show()


def present_fftseq(seq):
    p = plot_fftseq(seq)
    p.show()


def show_line(line, title=None):
    p = plot_line(line)
    filename = '/tmp/' + \
        ''.join(random.sample(string.ascii_letters+string.digits, 8))+'.png'
    p.savefig(filename)
    p.close()
    im = Image.open(filename)
    im.show(title=title)


def show_fftseq(seq, title=None):
    p = plot_fftseq(seq)
    filename = '/tmp/' + \
        ''.join(random.sample(string.ascii_letters+string.digits, 8))+'.png'
    p.savefig(filename)
    p.close()
    im = Image.open(filename)
    im.show(title=title)


def apply_seq(func, fftseq, apseq):
    afseq = np.zeros(fftseq.shape, dtype=fftseq.dtype)
    afseq[:len(apseq)] = apseq
    if len(fftseq) % 2 == 0:
        afseq[len(apseq):] = apseq[::-1]
    else:
        afseq[len(apseq):] = apseq[:0:-1]
    return func(fftseq, afseq)


def get_apply_length(seq):
    seqlength = (len(seq) + 1) // 2
    return seqlength


def view_instances(start_point, angle, length, filelist, bias=None):
    '''
    observe the color features of specific linear set in the image list.

    :param start_point: a base point that the line starts at. eg [x,y]
    :param angle:       the direction in degrees. like 270...
    :param length:      the length of the line.
    :param filelist:    filenames in a list.
    :param bias:        the bias position and angle of each image.[x,y,angle]
    '''

    # image_list = []
    # jch_list = []
    # s_point_list = []
    colora = 0.1
    colorb = 0.6
    colorc = 0.4

    p1 = plt.subplot(211)
    tmptitle = str(start_point[0]) + "," + str(start_point[1]) + \
        " " + str(angle) + ' ' + str(length) + ' ' + \
        ' '.join(filelist)
    p1.set_title(tmptitle, fontsize=12)
    p2 = plt.subplot(212)

    for i in range(len(filelist)):
        im = Image.open(filelist[i])
        s_point = start_point
        # s_point2 = start_point
        ang = angle
        # theta = 0
        if bias is not None:
            bias_p = bias[i]
            ang = ang + bias_p[2]
            s_point = [s_point[0]+bias_p[0], s_point[1]+bias_p[1]]
        theta = ang * np.pi / 180
        s_point1 = [s_point[0] + np.cos(theta + np.pi/2) * 1.5,
                    s_point[1] - np.sin(theta + np.pi/2) * 1.5]
        s_point2 = [s_point[0] + np.cos(theta - np.pi/2) * 1.5,
                    s_point[1] - np.sin(theta - np.pi/2) * 1.5]
        jch, rgb = get_line(im, s_point, ang, length)
        x = np.arange(len(jch))
        # jch_list.append(jch)
        e_point1 = [length * np.cos(theta) + s_point1[0],
                    -length * np.sin(theta) + s_point1[1]]
        e_point2 = [length * np.cos(theta) + s_point2[0],
                    -length * np.sin(theta) + s_point2[1]]
        draw = ImageDraw.Draw(im)
        draw.line(s_point1 + e_point1, fill=(255, 255, 0), width=2)
        draw.line(s_point2 + e_point2, fill=(255, 255, 0), width=2)
        im.show()
        p1.plot(x, jch[:, 0], '|-', color=(colora, colorb, colorc))  # ,
# label=filelist[i]+"-j")
        p1.plot(x, jch[:, 1], '|-', color=(colorb, colorc, colora))  # ,
# label=filelist[i]+'-c')
        p1.plot(x, jch[:, 2]/4, '|-', color=(colorb, colora, colora))  # ,
# label=filelist[i]+'-h')
        fftj = np.log10(np.fft.fftshift(np.abs(np.fft.fft(jch[:, 0]))) + 1)
        fftc = np.log10(np.fft.fftshift(np.abs(np.fft.fft(jch[:, 1]))) + 1)
        ffth = np.log10(np.fft.fftshift(np.abs(np.fft.fft(jch[:, 2]))) + 1)
        p2.plot(x, fftj, color=(colora, colorb, colorc))  # ,
# label=filelist[i]+'-j')
        p2.plot(x, fftc, color=(colorb, colorc, colora))  # ,
# label=filelist[i]+'-c')
        p2.plot(x, ffth, color=(colorb, colora, colora))  # ,
#  label=filelist[i]+'-h')
        colora = colora**0.8   # np.fmod( colora + 0.4 ,1.0)
        colorb = colorb**0.3   # np.fmod( colorb + 0.4 ,1.0)
        colorc = colorc**0.5   # np.fmod( colorc + 0.4 ,1.0)

    p1.set_xticks(np.arange(length//10) * 10)
    p1.set_yticks(np.arange(100//10) * 10)
    p1.grid(True)
    p1.legend()
    p2.set_xticks(np.arange(length//10) * 10)
    # p1.yticks(np.arange(100//10) * 10)
    p2.grid(True)
    p2.legend()
    # plt.legend()
    plt.show()
