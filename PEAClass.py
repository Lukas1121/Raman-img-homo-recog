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

class PEA:
    def __init__(self,path):
        self.files = self.unpack_files(path)

    def unpack_files(self,path):
        files = []
        for f in glob.glob(path + "/*"):
            files.append(cv2.imread(f))
        return files

    def show_files(self):
        for f in self.files:
            cv2.imshow("img",f)
            cv2.waitKey(0)

    def edge_detect_boundaries(self,img=int):
        self.crop_img(img)
        img_gray = cv2.cvtColor(self.files[img],cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray,(3,3),0)
        edges = cv2.Canny(img_gray,threshold1=150,threshold2=170)
        cv2.imshow("dege detected image",edges)
        cv2.imshow("cropped image",self.files[img])
        cv2.waitKey(0)

    def crop_img(self,img=int):
        self.files[img] = self.files[img][0:-(60),(60):-1]