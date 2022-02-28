import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class Main:
    def __init__(self,files):
        self.files = files

    def average_pixels(self,img):
        print(np.average(img))
        cv2.imshow("something", img)
        cv2.waitKey(0)

    def average_all_img(self):
        self.averages = []
        for f in self.files:
           self.averages.append(np.average(f))
        return self.averages

    def find_min_max_images(self):
        idx_min = np.argmin(self.averages,axis=0)
        idx_max = np.argmax(self.averages,axis=0)
        cv2.imshow("inhomogeneous",self.files[idx_min])
        cv2.imshow("homoegeneous",self.files[idx_max])
        cv2.waitKey(0)

    def average_voxels(self,img=int,show_img=False):
        vox_avg = []
        temp = []
        for n in range(1,150):
            temp.clear()
            for (i) in range((1+(3*(n-1))),(3*n)):
                for j in range((1+(3*(n-1))),(3*n)):
                    temp.append(self.files[img][i,j])
                vox_avg.append(sum(temp)/len(temp))
        self.hist_plot(vox_avg)
        if show_img:
            cv2.imshow("blehh",self.files[img])
            cv2.waitKey(0)
        return vox_avg

    def hist_plot(self,vox_avg):
        vox_avg.sort()
        vox_avg = self.remove_outliers(vox_avg,np.std(vox_avg),np.mean(vox_avg))
        y = stats.norm.pdf(vox_avg,np.mean(vox_avg),np.std(vox_avg))*6
        plt.figure()
        plt.hist(vox_avg,bins=30)
        plt.plot(vox_avg,y)
        plt.show()

    def remove_outliers(self,lst,sigma,mu):
        idx_list = []
        for i in range(0,len(lst)):
            if lst[i] > (mu+2*sigma) < lst[i]:
                idx_list.append(i)
        lst = np.delete(lst,obj=idx_list)
        return lst

    def extract_all_img_homogeneity(self):
        arr = []
        for i in range(len(self.files)):
            vox_avg = self.average_voxels(i,show_img=False)
            arr.append([vox_avg,i])
        self.arr=arr








