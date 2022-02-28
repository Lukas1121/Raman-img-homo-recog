import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy import stats
import sys
sys.path.append("External_Functions")
from ExternalFunctions import nice_string_output, add_text_to_ax

class Main:
    def __init__(self,files,boundaries=(5,130)):
        self.files = files
        self.rem_outliers = None
        self.plot = None
        self.boundaries = boundaries

    def average_pixels(self,img):
        print(np.average(img))
        cv2.imshow("something", img)
        cv2.waitKey(0)

    def average_all_img(self):
        self.averages = []
        for f in self.files:
           self.averages.append(np.average(f))
        return self.averages

    def min_max_idx(self):
        temp = []
        for i in range(len(self.arr)):
            temp.append(np.std(self.arr[i][:]))
        idx_min = np.argmin(temp, axis=0)
        idx_max = np.argmax(temp, axis=0)
        fig, axes = plt.subplots(nrows=2, ncols=2)

        axes[0][1].hist(self.arr[idx_min][:],bins=30) #plotting histogram
        axes[0][1].plot(self.arr[idx_min][:],
                        stats.norm.pdf(self.arr[idx_min][:],np.mean(self.arr[idx_min][:]),np.std(self.arr[idx_min][:])),
                        c="r") #plotting norm pdf
        axes[0][0].imshow(self.files[idx_min])
        axes[0][0].set_title("homoegenoust")

        d_min = {"mean": np.mean(self.arr[idx_min][:]),
             "std": np.std(self.arr[idx_min][:])}
        d_max = {"mean": np.mean(self.arr[idx_max][:]),
                 "std": np.std(self.arr[idx_max][:])}

        text1 = nice_string_output(d_min, extra_spacing=2, decimals=3)
        text2 = nice_string_output(d_max, extra_spacing=2, decimals=3)
        add_text_to_ax(0.02, 0.97, text1, axes[0][1], fontsize=12)
        add_text_to_ax(0.02, 0.97, text2, axes[1][1], fontsize=12)

        axes[1][1].hist(self.arr[idx_max][:], bins=30)
        axes[1][1].plot(self.arr[idx_max][:],
                        stats.norm.pdf(self.arr[idx_max][:], np.mean(self.arr[idx_max][:]),np.std(self.arr[idx_max][:])),
                        c="r")
        axes[1][0].imshow(self.files[idx_max])
        axes[1][0].set_title("inhomogenoust")

        rect0 = patches.Rectangle((self.boundaries[0], self.boundaries[0]), self.boundaries[1] * 3,
                                 self.boundaries[1] * 3, linewidth=3, edgecolor='r', facecolor='none')
        rect1 = patches.Rectangle((self.boundaries[0], self.boundaries[0]), self.boundaries[1] * 3,
                                 self.boundaries[1] * 3, linewidth=3, edgecolor='r', facecolor='none')

        axes[0][0].add_patch(rect0)
        axes[1][0].add_patch(rect1)

        fig.tight_layout()
        plt.show()

    def average_voxels(self,img=int,show_img=False):
        vox_avg = []
        temp = []
        for n in range(self.boundaries[0],self.boundaries[1]):
            temp.clear()
            for (i) in range((1+(3*(n-1))),(3*n)):
                for j in range((1+(3*(n-1))),(3*n)):
                    temp.append(self.files[img][i,j])
                vox_avg.append(sum(temp)/len(temp))
        if self.plot:
            self.hist_plot(vox_avg,idx=img)
        if show_img:
            cv2.imshow("blehh",self.files[img])
            cv2.waitKey(0)
        return vox_avg

    def hist_plot(self,vox_avg,idx=int):
        vox_avg.sort()
        if self.rem_outliers:
            vox_avg = self.remove_outliers(vox_avg,np.std(vox_avg),np.mean(vox_avg))
            print("Removing outliers")
        y = stats.norm.pdf(vox_avg,np.mean(vox_avg),np.std(vox_avg))
        fig, axes = plt.subplots(nrows=2, ncols=1)

        axes[0].hist(vox_avg,bins=30)

        d = {"mean":np.mean(vox_avg),
             "std":np.std(vox_avg)}

        text = nice_string_output(d, extra_spacing=2, decimals=3)
        add_text_to_ax(0.02, 0.97, text, axes[0], fontsize=14)

        axes[0].set_xlim((np.mean(vox_avg)-4*np.std(vox_avg),np.mean(vox_avg)+4*np.std(vox_avg)))
        axes2 = axes[0].twinx()
        axes2.plot(vox_avg,y,c="r")

        axes[1].imshow(self.files[idx])
        rect = patches.Rectangle((self.boundaries[0], self.boundaries[0]), self.boundaries[1]*3, self.boundaries[1]*3, linewidth=3, edgecolor='r', facecolor='none')
        axes[1].add_patch(rect)
        fig.tight_layout()
        plt.show()

    def remove_outliers(self,lst,sigma,mu):
        idx_list = []
        for i in range(0,len(lst)):
            if lst[i] > (mu+3*sigma) < lst[i]:
                idx_list.append(i)
        lst = np.delete(lst,obj=idx_list)
        return lst

    def extract_all_img_homogeneity(self,rem_outliers=False,plot=True):
        if rem_outliers:
            self.rem_outliers=rem_outliers
        if plot:
            self.plot = True
        arr = []
        for i in range(len(self.files)):
            vox_avg = self.average_voxels(i,show_img=False)
            arr.append(vox_avg)
        self.arr=arr
        return arr








