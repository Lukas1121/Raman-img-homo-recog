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
        self.files[img] = self.files[img][0:-(25),(25):-1]
        return self.files[img]

    def find_countours(self,img=int):
        gray_img = cv2.cvtColor(self.files[img],cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray image",gray_img)
        blur = cv2.medianBlur(gray_img,7)
        # cv2.imshow("blurred",blur)
        canny = cv2.Canny(blur,125,175)
        # cv2.imshow("Canny image",canny)

        contours, _ = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.waitKey(0)
        return contours

    def plot_contours(self,contours,img=int):
        plt.figure()
        plt.plot(contours[:][0],contours[:][1])



"""

    def average_kernels(self,img=int):
        B_vox_avg = []
        R_vox_avg = []
        G_vox_avg = []
        n = 0
        temp = []
        while True:
            n += 1
            if self.kernel[0]*(n) >= len(self.files[img]):
                return (B_vox_avg,R_vox_avg,G_vox_avg)
            for _ in range(len(self.files[img])-1):
                temp.clear()
                for i in range((self.kernel[0]*(n-1)),self.kernel[0]*n):
                    for j in range((self.kernel[0]*(n-1)),self.kernel[0]*n):
                        temp.append(self.files[img][i][j])
                print(temp)
                B_vox_avg.append(sum(temp[:][0])/len(temp[:][0]))
                R_vox_avg.append(sum(temp[:][1])/len(temp[:][1]))
                G_vox_avg.append(sum(temp[:][2]) / len(temp[:][2]))

    def average_with_c_function(self,lst):
        average = []
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                average[i][0].append(sum(lst[i][j][0])/len(lst[i][j]))
                average[i][1].append(sum(lst[i][j][1]) / len(lst[i][j]))
                average[i][2].append(sum(lst[i][j][2]) / len(lst[i][j]))
        return average

"""

