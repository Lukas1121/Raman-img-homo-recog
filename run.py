import numpy as np
# from bin import image_treatment
# from bin import avg_by_kernel
from bin import PEAClass

path = "Raman\Blind_test"


kernel = np.array([[-1,-1,-1],
                  [-1, 9,-1],
                  [-1,-1,-1]])

sharpen_kernel = np.array([[0,-1,0],
                           [-1,5,-1],
                           [0,-1,0]])

obj = PEAClass.Main(path=path)

# obj.find_countours(img=0,
#                    show_img=True)

obj.loop_through_all_img(use_L_or_A="L",
                         save_img=True,
                         max_idx_range=10)

# obj.custom_kernel_processing(kernel=sharpen_kernel,
#                              img=3,
#                              save_plot=False)

