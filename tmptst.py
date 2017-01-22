#!ipython
# a = 100
# b = Image.open('compare_1.jpg')

from imfft import *

'''
a = np.zeros(100)
a[40:60] = 100

fa = np.fft.fft(a)
show_fftseq(fa)

a[30:40] = np.arange(10) * 10
a[60:70] = np.arange(10)[::-1] * 10
show_line(a)
e = get_apply_length(a)
seq = np.linspace(2**0.5, 1.0, e) ** 2
fa_a = apply_seq(lambda x, y: x*y, fa, seq)
seq2 = (np.logspace(2, 0, e) - 1) / 99 + 1
fa_b = apply_seq(lambda x, y: x*y/2, fa, seq2)
seq3 = (np.logspace(3, 0, e) - 1) / 999 + 1
fa_c = apply_seq(lambda x, y: x*y/2, fa, seq3)
seq4 = (np.logspace(8, 0, e) - 1) / (10 ** 8 - 1) + 1
fa_d = apply_seq(lambda x, y: x*y/2, fa, seq4)

seq5 = (np.logspace(0, 8, e) - 1) / (10 ** 8 - 1) + 1
fa_5 = apply_seq(lambda x, y: x*y/2, fa, seq5)
show_line(seq5)
show_fftseq(fa_5)

seq6 = (np.logspace(0, 2, e) - 1) / (10 ** 2 - 1) + 1
fa_6 = apply_seq(lambda x, y: x*y/2, fa, seq6)

# 区间消除
seq7 = np.linspace(1, 1, e)
seq7[e*9//10:e*10//10] = 0.0
fa_7 = apply_seq(lambda x, y: x*y, fa, seq7)
show_line(seq7)
show_fftseq(fa_7)


seq8 = np.linspace(1, 1, e)
seq8[e*8//10:e*9//10] = 0.0
fa_8 = apply_seq(lambda x, y: x*y, fa, seq8)
show_line(seq8)
show_fftseq(fa_8)

seq9 = np.linspace(1, 1, e)
seq9[e*7//10:e*8//10] = 0.0
fa_9 = apply_seq(lambda x, y: x*y, fa, seq9)
show_line(seq9)
show_fftseq(fa_9)

seq10 = np.linspace(1, 1, e)
seq10[e*6//10:e*7//10] = 0.0
fa_10 = apply_seq(lambda x, y: x*y, fa, seq10)
show_line(seq10)
show_fftseq(fa_10)
'''

for i in range(0, 5):
    seq = np.linspace(1, 1, e)
    seq[e*i//10:e*(i+1)//10] = 0.0
    fac = apply_seq(lambda x, y: x*y, fa, seq)
    show_fftseq(fac)


seq11 = np.zeros(120)
seq11[:50] = fa[:50]
seq11[50:60] = fa[40:50]
seq11[60:70] = fa[50:60]
seq11[70:] = fa[50:]
show_fftseq(seq11)

image = Image.open('compare_1.jpg')
line = get_line(image, [100, 400], 30, 300)
view_instances([100, 400], 30, 300, ['compare_1.jpg'])

lilen = get_apply_length(line)
seqli = np.linspace(1, 2, lilen)
linefft = np.fft.fft(line[:, 0])

line_f1 = apply_seq(lambda x, y: x*y, linefft, seqli)
show_fftseq(line_f1)

seqli2 = np.linspace(1, 0.5, lilen)
line_f2 = apply_seq(lambda x, y: x*y, linefft, seqli2)

l2 = get_line(image, [0, 300], 0, 600)


pa = pylab.subplot(211)
pa.grid(True)
pb = pylab.subplot(212)
pb.grid(True)
pa.plot(jch[50:150, 0], '|-', color=(0.1, 0.1, 0.1))
pa.plot(jch[50:150, 1], '|-', color=(0.5, 0.5, 0.5))
pa.plot(jch[50:150, 2], '|-', color=(0.9, 0.1, 0.1))
pb.plot(rgb[50:150, 0], '|-', color=(0.8, 0.1, 0.1))
pb.plot(rgb[50:150, 1], '|-', color=(0.1, 0.7, 0.1))
pb.plot(rgb[50:150, 2], '|-', color=(0.1, 0.1, 0.7))
