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
    def __init__(self,path,patch_scan_size=3,binary=True):
        self.files = self.package_img_to_array(path)
        # self.files = self.files[95:105]
        self.rem_outliers = None
        self.plot = None
        self.patch_scan_size = patch_scan_size
        self.boundaries = [0,0]

    def loop_boundaries(self):
        for i in range(len(self.files)):
            self.define_boundaries(img=i)

    def define_boundaries(self,img=int):
        h, w = self.files[img].shape
        if h < w:
            residuals = (h%self.patch_scan_size)
            self.boundaries[1] = round(w/self.patch_scan_size-residuals)
        else:
            residuals = (w%self.patch_scan_size)
            self.boundaries[1] = round(h/self.patch_scan_size-residuals)
        return self.boundaries

    def package_img_to_array(self,path):
        files = []
        for f in glob.glob(path + "/*"):
            files.append(cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)/255)
        return files

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
        # axes[0][1].set_xlim(0.3,0.9)
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
        self.boundaries = self.define_boundaries(img=img)
        vox_avg = []
        temp = []
        for n in range(self.boundaries[0],self.boundaries[1]-self.patch_scan_size):
            temp.clear()
            for (i) in range((1+(self.patch_scan_size*(n-1))),(self.patch_scan_size*n)):
                for j in range((1+(self.patch_scan_size*(n-1))),(self.patch_scan_size*n)):
                    temp.append(self.files[img][i,j])
                vox_avg.append(sum(temp)/len(temp))
        if self.plot:
            self.hist_plot(vox_avg,idx=img)
        if show_img:
            cv2.imshow("blehh",self.files[img])
            cv2.waitKey(0)
        self.vox_avg = vox_avg
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

    def min_max(self,lst):
        idx_max = np.argmax(lst)
        idx_min = np.argmin(lst)
        return (idx_min,idx_max)

    def plot_defects(self,img=int,avg_voxel_multiplier=None):
        avg_voxels = self.average_voxels(img=img)
        if avg_voxel_multiplier == None:
            print("clean list")
            idx_min,idx_max = self.min_max(lst=avg_voxels)
        else:
            print("averaging averages")
            new_avg_list = []
            for i in range(len(avg_voxels)):
                temp = 0
                for n in range(avg_voxel_multiplier):
                    temp += avg_voxels[i]/avg_voxel_multiplier
                new_avg_list.append(temp)
            idx_min, idx_max = self.min_max(lst=new_avg_list)

        fig, ax = plt.subplots()

        ax.imshow(self.files[img])

        rect0 = patches.Rectangle((idx_min, idx_min), 25, 25, linewidth=2, edgecolor='b', facecolor='none',label="min voxel avg.")
        rect1 = patches.Rectangle((idx_max, idx_max), 25, 25, linewidth=2, edgecolor='r', facecolor='none',label="max voxel avg.")

        ax.add_patch(rect0)
        ax.add_patch(rect1)

        plt.legend()

        fig.tight_layout()
        plt.show()

class DetectDefects(Main):
    def __init__(self,img=int,boundaries=(25,120)):
        self.vox_avg = self.average_voxels(img=img,show_img=False)
        self.img = self.files[img]
        self.boundaries = boundaries

    def min_max(self):
        idx_max = np.argmax(self.vox_avg)
        idx_min = np.argmin(self.vox_avg)
        return (idx_min,idx_max)

    def plot_defects(self,square_multiplier=3):
        idx_min,idx_max = self.min_max()

        fig, axes = plt.subplots(nrows=1,ncols=1)

        axes[0].imshow(self.img)

        rect0 = patches.Rectangle((idx_min, idx_min), 30, 30, linewidth=2, edgecolor='r', facecolor='none')
        rect1 = patches.Rectangle((idx_max, idx_max), 30, 30, linewidth=2, edgecolor='r', facecolor='none')

        axes[0].add_patch(rect0)
        axes[0].add_patch(rect1)

        fig.tight_layout()
        plt.show()

# class VideoFunc(Main):
#     def __init__(self,files,boundaries=(25,120)):
#         self.files = files
#         self.boundaries = boundaries
#
#     def average_voxels_vid(self,img=int):
#         vox_avg = []
#         temp = []
#         for n in range(self.boundaries[0],self.boundaries[1]):
#             temp.clear()
#             for (i) in range((1+(3*(n-1))),(3*n)):
#                 for j in range((1+(3*(n-1))),(3*n)):
#                     temp.append(self.files[img][i,j])
#                 vox_avg.append(sum(temp)/len(temp))
#                 self.hist_plot_vid(vox_avg,idx=img)
#         return vox_avg
#
#     def hist_plot_vid(self, vox_avg, idx=int):
#         vox_avg.sort()
#         if self.rem_outliers:
#             vox_avg = self.remove_outliers(vox_avg, np.std(vox_avg), np.mean(vox_avg))
#             print("Removing outliers")
#         y = stats.norm.pdf(vox_avg, np.mean(vox_avg), np.std(vox_avg))
#         plt.clf()
#         fig, axes = plt.subplots(nrows=2, ncols=1)
#
#         axes[0].hist(vox_avg, bins=30)
#
#         d = {"mean": np.mean(vox_avg),
#              "std": np.std(vox_avg)}
#
#         text = nice_string_output(d, extra_spacing=2, decimals=3)
#         add_text_to_ax(0.02, 0.97, text, axes[0], fontsize=14)
#
#         axes[0].set_xlim((np.mean(vox_avg) - 4 * np.std(vox_avg), np.mean(vox_avg) + 4 * np.std(vox_avg)))
#         axes2 = axes[0].twinx()
#         axes2.plot(vox_avg, y, c="r")
#
#         axes[1].imshow(self.files[idx])
#         rect = patches.Rectangle((self.boundaries[0], self.boundaries[0]), self.boundaries[1] * 3,
#                                  self.boundaries[1] * 3, linewidth=3, edgecolor='r', facecolor='none')
#         axes[1].add_patch(rect)
#         fig.tight_layout()
#         plt.savefig("temp/pic %s"%len(vox_avg))
#
#     def extract_all_img_homogeneity_vid(self,rem_outliers=False):
#         if rem_outliers:
#             self.rem_outliers=rem_outliers
#         else:
#             self.rem_outliers = rem_outliers
#         for i in range(len(self.files)):
#             self.average_voxels_vid(i)
#
#
#     def graph2vid(self, options='video',filename = "video",fpsrate=1, empty_dir_on_done=True): #turns a series of n pictures in directory into a video of the .avi type or a gif
#         self.img_save_dir = "temp"
#         list1 = os.listdir(self.img_save_dir)
#
#         img_array = []
#
#         size = (640,480)
#
#         if options == 'video':
#             for i in range(len(list1)):
#                 img = cv2.imread(self.img_save_dir + '/pic %s.png' %(i))
#                 for n in range(fpsrate):
#                     img_array.append(img)
#                     if (i + 1) % (len(list1)) == 0:
#                         for i in range(fpsrate + 3):
#                             img_array.append(img)
#             out = cv2.VideoWriter(filename + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
#
#             for i in range(len(img_array)):
#                 out.write(img_array[i])
#             out.release()
#             print('Video made')
#         if empty_dir_on_done == True:
#             files = glob.glob(self.img_save_dir+'/*')
#             for f in files:
#                 os.remove(f)