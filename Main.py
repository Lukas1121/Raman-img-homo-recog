import cv2
import glob
import mainClass as _

path = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"

files = []

for f in glob.glob(path+"/*"):
    files.append(cv2.resize(cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)/255,(420,420))) #normalizing and storing images to list

obj = _.Main(files,boundaries=(25,120))


# obj.average_voxels(img=10,show_img=True)
arr = obj.extract_all_img_homogeneity(rem_outliers=True,plot=False)
obj.min_max_idx()
# obj.plot_defects(img=17)



# vid = _.VideoFunc(files=files[10])
# vid.extract_all_img_homogeneity_vid()
# vid.graph2vid()