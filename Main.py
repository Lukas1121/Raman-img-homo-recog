import cv2
import glob

import matplotlib.pyplot as plt

import mainClass as _
import test as test
import PEAClass as PEA

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\PEA\img"

# obj = _.Main(path_hery)
# obj_PEA = PEA.PEA(path_PEA)
obj_test = test.Main(path=path_PEA,kernel=(5,5))
obj_test.get_img_shape(img=3)
# img = obj_test.show_img(img=3)
contours = obj_test.find_countours(img=3)

for i in range(len(contours)):




# obj_PEA.edge_detect_boundaries(img=3)

# obj.average_voxels(img=10,show_img=True)
# obj.extract_all_img_homogeneity(rem_outliers=True,plot=True)
# obj.min_max_idx()
# obj.plot_defects(img=10)



# vid = _.VideoFunc(files=files[10])
# vid.extract_all_img_homogeneity_vid()
# vid.graph2vid()