File to graphic image encoder/decoder
=====================================

Virtual machines, like VMWare, in some configurations, do not have file download
functionality but still allow to do PrintScreen of the VM window into the local clipboard.
So there is a workaround for downloading a file: encode a file into a graphical image,
then copy and paste the image into a graph editor in the local machine,
then save into a graph file, then decode the image into a local file.
File size is limited by max image size that can be drawn on the screen.
For this program max file size is 64k bytes.

First utility creates a separate window with graphical image of encoded file.
User should switch to local system and do PrtScreen for the VM window, paste the image in
a graphical editor (Windows Paint), crop the encoded part (leaving few pixels as margins),
save into a PNG file. 
Then run the second utility on local machine, decoding image into the original file.

System requirements:
===================
 - In VM machine: Python 3 with standard libraries (TkInter should be included)
 - In local machine: Python 3 with standard libraries + pillow (PIL) library

Notes:
=====
 - File size must not exceed 64k bytes, zipping recommended for larger files
 - It was tested in VMWare but probably will work with other VM hosts too
 - VM client must receive lossless B/W graphics from the host, color information may be lossy
 - save image into a lossless format, like PNG

Usage:
=====
ef <bytes_in_line> <filename>  
 - encodes a file into a graphical image

df <imagefile>  
 - decodes data from a graphical file into a file in current directory, file is named as original file

Example:
========
python ef.py 64 myfile.zip  
python df.py myfile.png

Image format:
=================
One pixel corresponds to one bit of data.
Each byte of data is encoded by 8 consecutive pixels, black for 1, white for 0.
Number of bytes in one image line is set by <bytes_in_line> parameter.
<bytes_in_line> typical value is between 32 and 128, depends on screen resolution

1st line:
8 bit   0xFFh synch bar  
16 bit  <bytes_in_line>  
16 bit  file size in bytes, big-endian  
var     file name encoded, ended by 0x0  

2nd and consecutive lines:
file data  
