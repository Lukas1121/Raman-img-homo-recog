import cv2
import numpy
import glob
import os

class Main(object):
    def __init__(self,path):
        self.files, self.filepaths = self.unpack_files(path=path)

    def unpack_files(self, path):
        files = []
        filenames = []
        for f in glob.glob(path + "/*"):
            files.append(cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY) / 255)
            filenames.append(os.path.basename(f))
        return self.crop_img(files), filenames

    def crop_img(self, files):
        for i in range(len(files)):
            files[i] = files[i][:-(60), 60:]
        return files

    def show_img(self, img=int):
        cv2.imshow("%s" % self.filenames[img], self.files[img])
        cv2.waitKey(0)

    def img_shape(self, img=int):
        w, h = self.files[img].shape
        return (w, h)

    def custom_kernel_processing(self,kernel,img=int,save_plot=False):
        sharpen = cv2.filter2D(self.files[img],-1,kernel=kernel)
        cv2.imshow("{0} w/ custom kernel".format(self.filepaths[img]),sharpen)
        cv2.imshow("{0}".format(self.filepaths[img]),self.files[img])
        cv2.waitKey(0)
        if save_plot:
            sharpen = sharpen*255
            cv2.imwrite("data/treated_images/{0}_sharpened.jpg".format(os.path.splitext(self.filepaths[img])[0]),sharpen)

    def N_custom_kernal_processing(self,kernel1,kernel2,img=int,save_plot=False):
        sharpen1 = cv2.filter2D(self.files[img],-1,kernel=kernel1)
        sharpen2 = cv2.filter2D(self.files[img],-1,kernel=kernel2)
        cv2.imshow("{0} w/ custom kernel1".format(self.filepaths[img]),sharpen1)
        cv2.imshow("{0} w/ custom kernel2".format(self.filepaths[img]),sharpen2)
        cv2.imshow("{0}".format(self.filepaths[img]),self.files[img])
        cv2.waitKey(0)
        if save_plot:
            sharpen = sharpen1*255
            cv2.imwrite("data/treated_images/{0}_sharpened.jpg".format(os.path.splitext(self.filepaths[img])[0]),sharpen)