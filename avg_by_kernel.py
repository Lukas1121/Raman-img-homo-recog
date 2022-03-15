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
        self.files,self.filenames = self.unpack_files(path)


    def unpack_files(self,path):
        files = []
        filenames = []
        for f in glob.glob(path + "/*"):
            files.append(cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)/255)
            filenames.append(os.path.basename(f))
        return self.crop_img(files), filenames

    def crop_img(self,files):
        for i in range(len(files)):
            files[i] = files[i][:-(60),60:]
        return files

    def show_img(self,img=int):
        cv2.imshow("%s"%self.filenames[img],self.files[img])
        cv2.waitKey(0)

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
        temp_idx = []
        avg = []
        patch_idx = []
        for i in range(int(self.img_search_range(img=img))-1):
            temp.clear()
            temp_idx.clear()
            for j in range(self.kernel*i,self.kernel*(i+1)):
                for n in range(self.kernel*i,self.kernel*(i+1)):
                    temp.append(self.files[img][j][n])
                    temp_idx.append([j,n])
            patch_idx.append([temp_idx[0],temp_idx[-1]])
            avg.append(sum(temp)/len(temp))
        return avg,patch_idx

    def max_avg_values(self,avg,n=5): #this is for getting the correct indeces of the averages to be used to get the indeces that draw the rectangles from patch_idx
        copied_avg = self.remove_outliers(avg,np.std(avg),np.mean(avg))
        idx_list = np.argpartition(copied_avg, -n)[-n:]
        return idx_list

    def remove_outliers(self,lst,sigma,mu): #removes avg values 3 sigma away from mean
        idx_list = []
        for i in range(0,len(lst)):
            if lst[i] > (mu+3*sigma) < lst[i]:
                idx_list.append(i)
            if lst[i] >=0.95:
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

        axes[1].imshow(self.files[img],cmap="gray",vmin=0,vmax=1)
        axes[1].set_title("%s"%self.filenames[img])
        fig.tight_layout()
        plt.show()

    def plot_ROI(self,avg,patch_idx,img=int,enlarge_rect=1):

        idx_avg_max_list = self.max_avg_values(avg)
        print(idx_avg_max_list[:])
        fig, ax = plt.subplots()

        ax.imshow(self.files[img],cmap="gray",vmin=0,vmax=1)

        for i in range(len(idx_avg_max_list)):
            ax.add_patch(patches.Rectangle((patch_idx[idx_avg_max_list[i]][0]),
                                           self.kernel*enlarge_rect, self.kernel*enlarge_rect,
                                           linewidth=1,
                                           edgecolor='r',
                                           facecolor='none',
                                           label="max voxel avg %s"%(i+1)))

        plt.legend()
        plt.title(self.filenames[img])
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



"""
DUMP

    def edge_detect_scale(self,img=int):
        true_pixel_value = self.files[img]*255
        blur = cv2.GaussianBlur(true_pixel_value,(13,13),0).astype("uint8")
        # blur = cv2.medianBlur(self.files[img],3)
        canny = cv2.Canny(blur,0,150)
        cv2.imshow("%s"%self.filenames[img],canny)
        cv2.waitKey(0)

"""