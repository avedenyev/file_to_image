# -------------------------------------------------
# usage: python ef.py <BIL> <file>
# -------------------------------------------------

from tkinter import *
from sys import argv
from math import floor

if len(argv) < 3:
	print("Wrong arguments")
	exit(1)

BIL = int(argv[1])
# LNS = int(argv[2])
FNM = argv[2]
X0 = 10
Y0 = 10	

# -------------------------------------------------
master = Tk()

canvas_width = BIL*8+40
canvas_height = 800
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

# -- create conversion tab --
convtab = []
for i in range(0,256):
	a = 0;
	if (i & 1) > 0: a |= 128
	if (i & 2) > 0: a |= 64
	if (i & 4) > 0: a |= 32
	if (i & 8) > 0: a |= 16
	if (i & 16) > 0: a |= 8
	if (i & 32) > 0: a |= 4
	if (i & 64) > 0: a |= 2
	if (i & 128) > 0: a |= 1
	convtab.append(a)

# print(convtab)	


bm_start = """
# define im_width 8
# define im_height 1
static char im_bits[] = {
"""

bm_end = """
};
"""

# -- create bitmap tab ------
bmtab = []
for i in range(0,256):
	bm = bm_start + hex(convtab[i]) + bm_end;
	bmtab.append(BitmapImage(data=bm))
#	w.create_image(10,i+2,image=bmtab[i],anchor="w")


# -- do the file ------
file = open(FNM, "rb")
bytes = file.read()
N = len(bytes)
i = 0

while i < N:
	x = X0 + (i*8) % (BIL*8)
	y = Y0 + floor(i/BIL)
	w.create_image(x, y, image=bmtab[bytes[i]], anchor="w")
	i += 1

file.close()

# -- put header -------
w.create_image(X0, Y0-1, image=bmtab[255], anchor="w")
flen_b = N.to_bytes(2,'little')
w.create_image(X0+8, Y0-1, image=bmtab[flen_b[0]], anchor="w")
w.create_image(X0+16,Y0-1, image=bmtab[flen_b[1]], anchor="w")

bil_b = BIL.to_bytes(1,'little')
w.create_image(X0+24,Y0-1, image=bmtab[bil_b[0]], anchor="w")

i = 0
for c in FNM:
	w.create_image(X0+32+i*8, Y0-1, image=bmtab[ord(c)], anchor="w")
	i += 1

w.create_image(X0+32+i*8, Y0-1, image=bmtab[0], anchor="w")
i += 1
w.create_image(X0+32+i*8, Y0-1, image=bmtab[255], anchor="w")

master.mainloop()
