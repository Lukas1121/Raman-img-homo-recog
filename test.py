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
        canny = cv2.Canny(blur,0,125)
        # cv2.imshow("Canny image",canny)
        contours, _ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow("Original image untreated", self.files[img])
        # img0 = cv2.drawContours(self.files[img], contours, -1, (0, 0, 0), 1)
        # cv2.imshow("Original img w/ contours",img0)
        # cv2.waitKey(0)
        return contours,self.files[img]

    def contour_to_A(self,contours,max_idx_range=5):
        A_list = []
        max_idx = []
        max_list = []
        for i in range(len(contours)):
            A_list.append(cv2.contourArea(contours[i]))
        for i in range(max_idx_range):
            idx = [i for i, x in enumerate(A_list) if x == max(A_list)]
            max_idx.append(idx)
            max_list.append(A_list[idx[0]])
            A_list.pop(idx[0])
        return max_list,np.array(max_idx).ravel()

    def contour_to_L(self,contours,max_idx_range=5):
        A_list = []
        max_idx = []
        max_list = []
        for i in range(len(contours)):
            A_list.append(cv2.arcLength(contours[i],True))
        for i in range(max_idx_range):
            idx = [i for i, x in enumerate(A_list) if x == max(A_list)]
            max_idx.append(idx)
            max_list.append(A_list[idx[0]])
            A_list.pop(idx[0])
        return max_list, np.array(max_idx).ravel()


    def mark_ROI_from_contour_A(self,contours,idx_list,img=int):
        img0 = np.copy(self.files[img])
        for i in range(len(idx_list)):
            print(contours[idx_list[i]])
            cnt = contours[idx_list[i]]
            rect = cv2.minAreaRect(cnt)
            box = np.int0(cv2.boxPoints(rect))
            new_img = cv2.drawContours(img0,[box],0,(0,0,255),2)
        stacked_img = np.concatenate((self.files[img],new_img),axis=1)
        cv2.imshow("Original PEA left, ROI detected right",stacked_img)
        return stacked_img

    def loop_through_all_img(self,max_idx_range=10,save_img=False,use_L_or_A=int):
        for i in range(len(self.files)):
            print(i)
            contours, img = self.find_countours(img=i)
            if use_L_or_A == 1:
                max_list, max_idx = self.contour_to_L(contours, max_idx_range)
            if use_L_or_A == 2:
                max_list, max_idx = self.contour_to_A(contours, max_idx_range)
            stacked_img = self.mark_ROI_from_contour_A(contours, max_idx, img=i)
            if save_img:
                cv2.imwrite(("PEA/treated/treated_img_%s" % i + ".png"), stacked_img)
            cv2.waitKey(0)



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

