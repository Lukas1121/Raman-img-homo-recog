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

class PixelAvg:
    def __init__(self,path,kernel=3):
        self.kernel = kernel
        self.files = self.unpack_files(path)

    def unpack_files(self,path):
        files = []
        for f in glob.glob(path + "/*"):
            files.append(cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)/255)
        return self.crop_img(files)

    def crop_img(self,files):
        for i in range(len(files)):
            files[i] = files[i][20:-(20),(20):-20]
        return files

    def img_shape(self,img=int):
        w,h = self.files[img].shape
        return (w,h)

    def shortest_array(self,w,h):
        if w < h:
            return w
        else:
            return h

    def img_search_range(self,img=int):
        l = self.shortest_array(*self.img_shape(img=img))
        res = l%self.kernel
        return ((l-res)/self.kernel)

    def avg_by_kernel(self,img=int):
        temp = []
        avg = []
        for i in range(int(self.img_search_range(img=img))-1):
            temp.clear()
            for j in range(self.kernel*i,self.kernel*(i+1)):
                for n in range(self.kernel*i,self.kernel*(i+1)):
                    temp.append(self.files[img][j][n])
            avg.append(sum(temp)/len(temp))
        return avg

    def remove_outliers(self,lst,sigma,mu):
        idx_list = []
        for i in range(0,len(lst)):
            if lst[i] > (mu+3*sigma) < lst[i]:
                idx_list.append(i)
            if lst[i] >=0.9:
                idx_list.append(i)
        lst = np.delete(lst,obj=idx_list)
        return lst

    def hist_plot(self,vox_avg,img=int):
        vox_avg.sort()
        vox_avg = self.remove_outliers(vox_avg,np.std(vox_avg),np.mean(vox_avg))
        y = stats.norm.pdf(vox_avg,np.mean(vox_avg),np.std(vox_avg))
        fig, axes = plt.subplots(nrows=2, ncols=1)

        axes[0].hist(vox_avg,bins=(30))

        d = {"mean":np.mean(vox_avg),
             "std":np.std(vox_avg),
             "kernel":self.kernel}

        text = nice_string_output(d, extra_spacing=2, decimals=3)
        add_text_to_ax(0.02, 0.97, text, axes[0], fontsize=14)

        axes[0].set_xlim((np.mean(vox_avg)-4*np.std(vox_avg),np.mean(vox_avg)+4*np.std(vox_avg)))
        axes2 = axes[0].twinx()
        axes2.plot(vox_avg,y,c="r")

        axes[1].imshow(self.files[img])
        fig.tight_layout()
        plt.show()


    def min_max(self,lst):
        idx_max = np.argmax(lst)
        idx_min = np.argmin(lst)
        return (idx_min,idx_max)

    def plot_min_max_kernel_avg(self,avg,img=int):
        idx_min, idx_max = self.min_max(lst=avg)
        fig, ax = plt.subplots()

        ax.imshow(self.files[img])



        """ This needs some fixing up since the idx's er for the locations in a reduced list, their indices therefor do not reflect that of the images 
        
        NEEDS SOLUTION
        
        
        rect0 = patches.Rectangle((idx_min, idx_min), 25, 25, linewidth=2, edgecolor='b', facecolor='none',
                                  label="min voxel avg.")
        rect1 = patches.Rectangle((idx_max, idx_max), 25, 25, linewidth=2, edgecolor='r', facecolor='none',
                                  label="max voxel avg.")

        ax.add_patch(rect0)
        ax.add_patch(rect1)

        plt.legend()
        """

        fig.tight_layout()
        plt.show()

    def main_init(self,img=int,plot_distribution=True,plot_defects=True):
        avg = self.avg_by_kernel(img=img)
        if plot_distribution:
            self.hist_plot(avg,img=img)
        if plot_defects:
            self.plot_min_max_kernel_avg(avg,img=img)