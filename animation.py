import cv2
import avg_by_kernel

class Video():
    def __init__(self,arr,img):
        self.arr = arr
        self.img = img

    def graph2vid(self, fpsrate=1): #turns a series of n pictures in directory into a video of the .avi type or a gif
        w,h = self.img_arr[0].shape

        size = (w,h)

        out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30*fpsrate, size)

        for i in range(len(self.img_array)):
            out.write(self.img_array[i])
        out.release()
        print('Video made')

    def draw_rect(self):
        for i in range(len(self.arr)):
            
