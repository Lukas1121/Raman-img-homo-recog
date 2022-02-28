import cv2
import glob
import mainClass as _

path = "C:\\Users\Lukas\Documents\Master Thesis\Raman\Visible"

files = []

for f in glob.glob(path+"/*"):
    files.append(cv2.resize(cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)/255,(450,450))) #normalizing and storing images to list

obj = _.Main(files)

# obj.average_voxels(img=10,show_img=True)
obj.extract_all_img_homogeneity()