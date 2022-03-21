from bin import mainClass
from bin import avg_by_kernel

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\data\PEA\img"
path_hery_raw = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Herys Tirf"

obj = avg_by_kernel.PixelAvg(path_hery_raw)
obj.average_all_files()


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