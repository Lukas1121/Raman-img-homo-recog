import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy import stats
import os
import glob
import sys
sys.path.append("External_Functions")
from ExternalFunctions import nice_string_output, add_text_to_ax

class Main:
    def __init__(self,path,kernel = (3,3)):
        self.files = self.unpack_files(path)
        self.kernel = kernel

    def unpack_files(self, path):
        files = []
        for f in glob.glob(path + "/*"):
            files.append(cv2.imread(f)[0:-(60),(60):-1])
        return files

    def show_img(self,img=int):
        cv2.imshow("the image",self.files[img])
        cv2.waitKey(0)
        return self.files[img]

    def get_img_shape(self,img=int):
        h, w, c = self.files[img].shape
        return (h,w,c)

    def crop_img(self,img=int):
        self.files[img] = self.files[img][0:-(60),(60):-1]

    def average_kernels(self,img=int):
        vox_avg = []
        R_vox_avg = []
        G_vox_avg = []
        n = 0
        temp = []
        while True:
            n += 1
            if n == 10:
                return vox_avg
            for j in range(len(self.files[img][0][:])):
                temp.clear()
                for i in range(self.kernel[0]*n):
                    temp.append(self.files[img][i][j][:])
                vox_avg.append(temp)



