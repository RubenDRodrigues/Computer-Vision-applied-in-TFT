#!/usr/bin/python
from PIL import Image
import os, sys

path = "C:/Users/ruben/Desktop/TFTAI/YOLOv7/yolov7/train/images/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
  
        im = Image.open(path+item)
        f, e = os.path.splitext(path+item)
        imResize = im.resize((128,128), Image.ANTIALIAS)
        imResize.save(f + ".png", 'png', quality=100)

resize()