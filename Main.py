import animation as anim
import mainClass as _
import avg_by_kernel as avg
import PEAClass as PEA

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\PEA\img"
path_hery_raw = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Herys Tirf"

obj_hery = avg.PixelAvg(path_hery_raw,
                         kernel=7)

avg, patch_idx = obj_hery.avg_by_kernel(10)
print(len(patch_idx))
# vid_obj = anim.Video()




# idx_list = obj_hery.max_avg_values(avg)
#
# obj_hery.plot_ROI(avg,patch_idx,10,enlarge_rect=2)

# obj_hery.main_init(img=10,
#                    plot_defects=True,
#                    plot_distribution=True)




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