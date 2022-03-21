import numpy as np
from bin import image_treatment
from bin import avg_by_kernel
from bin import PEAClass

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\data\PEA\img"
path_hery_tirf = "Raman/herys_tirf/untreated"
path_SBA_15_PBS = "C:\\Users\lukas\Desktop\SBA-15a\SBA-15_a+PBS"
path_SBA_15 = "C:\\Users\lukas\Desktop\SBA-15a\SBA-15_a"
path_blind = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Blind_test"
path_Aaron = "C:\\Users\lukas\Desktop\Aaron"


kernel = np.array([[-1,-1,-1],
                  [-1, 9,-1],
                  [-1,-1,-1]])

sharpen_kernel = np.array([[0,-1,0],
                           [-1,5,-1],
                           [0,-1,0]])

obj = PEAClass.PEAClass(path=path_hery_tirf)

# obj.find_countours(img=3,show_img=True)

obj.loop_through_all_img(use_L_or_A="L",save_img=True)

# obj = image_treatment.Main(path=path_hery_tirf)

# obj.custom_kernel_processing(kernel=sharpen_kernel,
#                              img=3,
#                              save_plot=False)

# obj.N_custom_kernal_processing(kernel1=kernel,
#                                kernel2=sharpen_kernel,
#                                img=7)