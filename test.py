#!ipython
# -*- coding:utf-8 -*-

from imagealgo import *
from npcolorconvert import nprgb2jch, npjch2rgb
from PIL import ImageDraw


def show_instance(start_point, angle, length):

    f_1 = Image.open('compare_1.jpg')
    f_2 = Image.open('compare_3.jpg')

    s_point2 = [start_point[0] - 13, start_point[1] + 6]
    # rgb_1 = np.array(f_1)[400,50:350]
    # rgb_2 = np.array(f_2)[405,50:350]

    # jch_1 = nprgb2jch(rgb_1)a
    # jch_2 = nprgb2jch(rgb_2)
    jch_1 = get_line(f_1, start_point, angle, length)
    jch_2 = get_line(f_2, s_point2, angle, length)

    # for i in range(50,350):
    #    f_1.putpixel((i,398),(int(0xcc),int(0xff),int(0xff)))
    #    f_1.putpixel((i,402),(int(0xcc),int(0xff),int(0xff)))

    #    f_2.putpixel((i,403),(int(0xff),int(0xff),int(0xcc)))
    #    f_2.putpixel((i,407),(int(0xff),int(0xff),int(0xcc)))
    t_angle = angle * np.pi / 180.0
    end_point = [length * np.cos(t_angle) + start_point[0],
                 -length * np.sin(t_angle) + start_point[1]]
    e_point2 = [length * np.cos(t_angle) + s_point2[0],
                -length * np.sin(t_angle) + s_point2[1]]
    draw1 = ImageDraw.Draw(f_1)
    draw2 = ImageDraw.Draw(f_2)
    draw1.line(list(np.array(start_point + end_point) - 1), fill=(192, 0, 0))
    draw1.line(list(np.array(start_point + end_point) + 1), fill=(192, 0, 0))
    draw2.line(list(np.array(s_point2 + e_point2) - 1), fill=(192, 0, 0))
    draw2.line(list(np.array(s_point2 + e_point2) + 1), fill=(192, 0, 0))
    f_1.show()
    f_2.show()
    # f_1.close()
    # f_1.close()

    plt.plot(np.arange(len(jch_1)), jch_1[
             :, 0], '_-', color='#00aa88', label='1 j')
    plt.plot(np.arange(len(jch_2)), jch_2[
             :, 0], '_-', color='#00ffaa', label='2 j')
    plt.plot(np.arange(len(jch_1)), jch_1[
             :, 1], '_-', color='#cc9922', label='1 c')
    plt.plot(np.arange(len(jch_2)), jch_2[
             :, 1], '_-', color='#ffaa44', label='2 c')
    plt.plot(np.arange(len(jch_1)), jch_1[
             :, 2], '_-', color='#cc0066', label='1 h')
    plt.plot(np.arange(len(jch_2)), jch_2[
             :, 2], '_-', color='#ff00aa', label='2 h')
    plt.xticks(np.arange(length // 10) * 10)
    plt.yticks(np.arange(100 / 2) * 2)
    plt.grid(True, which='major')

    plt.legend()
    plt.show()

if __name__ == "__main__":
    show_instance([200, 100], -60, 300)
