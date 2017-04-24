#detect points for delaunay triangulations
import numpy as np
import cv2
import Tkinter as tk
import tkFileDialog
import random

def draw_delaunay(img, subdiv, delaunay_color ) :

    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList :

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

if __name__ == '__main__':
