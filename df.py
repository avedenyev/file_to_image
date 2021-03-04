# -------------------------------------------
# usage: python df.py <picfile.png>
# -------------------------------------------
from PIL import Image
from sys import argv
from math import floor

def read_byte(x,y):
    b1 = 1 if pix[x,y][0] < 127 else 0
    b2 = 1 if pix[x+1,y][0] < 127 else 0
    b3 = 1 if pix[x+2,y][0] < 127 else 0
    b4 = 1 if pix[x+3,y][0] < 127 else 0
    b5 = 1 if pix[x+4,y][0] < 127 else 0
    b6 = 1 if pix[x+5,y][0] < 127 else 0
    b7 = 1 if pix[x+6,y][0] < 127 else 0
    b8 = 1 if pix[x+7,y][0] < 127 else 0
    # print(b1,b2,b3,b4,b5,b6,b7,b8)
    return b1*128 + b2*64 + b3*32 + b4*16 + b5*8 + b6*4 + b7*2 + b8

# -----------------------------------------------------------------------
if len(argv) < 2:
    print("ERROR: Wrong arguments")
    exit(1)

im = Image.open(argv[1])
pix = im.load()
# print(im.size)  # Get the width and hight of the image for iterating over

# print(pix[1,1][0])  # Get the RGBA Value of the a pixel of an image
# print(pix[3,4][0])
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png

# ----- find x0, y0 -------
x0 = y0 = 0

for j in range(1, 40):
    for i in range(1, 20):
        if pix[i,j][0] < 127:
            x0 = i
            y0 = j
            break
    if x0 > 0:
        break

if x0 == 0 or y0 == 0:
    print("ERROR: Cannot find x0, y0")
    exit(1)

# ----- read file length -------
lo = read_byte(x0+8,y0)
hi = read_byte(x0+16,y0)
filelen = hi*256 + lo

print("File Length =", filelen)

if filelen <= 0 or filelen > 65535:
    print("ERROR: Wrong file length")
    exit(1)

# ----- read BIL -------
bil = read_byte(x0+24,y0)

print("Bytes In Line =", bil)

if bil <= 0:
    print("ERROR: Wrong BIL")
    exit(1)

# ----- read file name -------
fname_b = bytearray(64)
i = 0
x = x0+32
c = read_byte(x,y0)
while c > 0:
    fname_b[i] = c
    i += 1
    x += 8
    c = read_byte(x,y0)

fname = fname_b.decode("utf-8")
fname = fname[:fname.index("\x00")]
print("File Name =", fname)

# ----- read the data -------
data_b = bytearray(filelen)
for i in range(0, filelen):
    x = x0 + (i*8) % (bil*8)
    y = y0 + floor(i/bil) + 1
    data_b[i] = read_byte(x,y)

# ----- write data into file -------
outFile = open(fname, "wb")
outFile.write(data_b)
outFile.close()
