import cv2
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mainClass as _
import avg_by_kernel as avg
import PEAClass as PEA

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\PEA\img"

obj_hery = avg.PixelAvg(path_hery,
                         kernel=3)

obj_hery.main_init(img=10,
                   plot_defects=True,
                   plot_distribution=True)

# obj_PEA = PEA.Main(path=path_PEA,kernel=(5,5))
# obj_PEA.loop_through_all_img(use_L_or_A="L")
# contours = obj_PEA.find_countours(img=3)
# obj_Hery.show_img(img=7)
# obj_Hery.loop_through_all_img(use_L_or_A="A",max_idx_range=5)
# contours = obj_Hery.find_countours(img=10)
# obj_Hery.loop_through_all_img(use_L_or_A="A")



"""
cnt = contours[5]
M = cv2.moments(cnt)

rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
img_rect = cv2.drawContours(img,[box],0,(0,0,0),-1)
cv2.imshow("testing",img_rect)
cv2.waitKey(0)

Area = cv2.contourArea(cnt)
print(Area)

cx = int(M["m10"]/M["m00"])
cy = int(M["m01"]/M["m00"])

print(cx,cy)
"""