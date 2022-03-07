import cv2
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mainClass as _
import test as test
import PEAClass as PEA

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\Lukas\Documents\Master Thesis\Raman-img-homo-recog\PEA\img"

# obj = _.Main(path_hery)
# obj_PEA = PEA.PEA(path_PEA)
obj_test = test.Main(path=path_PEA,kernel=(5,5))
# obj_test.get_img_shape(img=3)
# img = obj_test.show_img(img=3)
contours,img = obj_test.find_countours(img=3)

max_list,max_idx = obj_test.contour_to_A(contours)

cnt = contours[max_idx[3]]

rect = cv2.minAreaRect(cnt)
box = np.int0(cv2.boxPoints(rect))
print(box)
img_rect = cv2.drawContours(img,[box],0,(0,0,255),-1)
cv2.imshow("testing",img_rect)
cv2.waitKey(0)



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



# df = pd.DataFrame(contours)
# print(df)



# for i in range(len(contours)):

"""